"""Command-line interface for the file-validator library.

Installed as the ``file_validator`` console script (see ``setup.py``).
"""
import argparse
import sys

from termcolor import colored

from file_validator import __version__
from file_validator.constants import (
    ALL,
    FILETYPE,
    MIMETYPES,
    PURE_MAGIC,
    PYTHON_MAGIC,
)
from file_validator.exceptions import (
    FileValidationException,
    LibraryNotSupportedException,
    SizeValidationException,
    TypeNotSupportedException,
)
from file_validator.utils import set_the_library
from file_validator.validators import FileValidator


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the command line interface."""
    parser = argparse.ArgumentParser(
        prog="file_validator",
        description=(
            "Validate files by mime type, extension, magic numbers and size."
        ),
    )
    parser.add_argument(
        "path",
        help="Path to the file to validate",
    )
    parser.add_argument(
        "--mimes",
        nargs="+",
        metavar="MIME",
        help="Acceptable mime types, e.g. image/png image/jpeg",
    )
    parser.add_argument(
        "--types",
        nargs="+",
        metavar="TYPE",
        help="Acceptable file types: image, audio, video, font, archive",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        metavar="EXTENSION",
        help="Acceptable file extensions, e.g. .png .jpg",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum allowed file size in bytes",
    )
    parser.add_argument(
        "--libraries",
        nargs="+",
        metavar="LIBRARY",
        help=(
            "Libraries used for mime validation: filetype, pure_magic, "
            "python_magic, mimetypes, django, all (default: all)"
        ),
    )
    parser.add_argument(
        "--django-mime",
        help=(
            "The content type guessed by Django (used with the django library)"
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _dispatch(file_validator: FileValidator, libraries: list) -> dict:
    """Run mime validation for every requested library."""
    for library in libraries:
        if library == ALL:
            file_validator.validate()
        elif library == PYTHON_MAGIC:
            file_validator.python_magic()
        elif library == PURE_MAGIC:
            file_validator.pure_magic()
        elif library == MIMETYPES:
            file_validator.mimetypes()
        elif library == FILETYPE:
            file_validator.filetype()
        else:
            file_validator.django()
    return file_validator.result_of_validation


def validate_file(args) -> dict:
    """Run the requested validations and return the results."""
    file_validator = FileValidator(
        file_path=args.path,
        libraries=args.libraries,
        acceptable_mimes=args.mimes,
        acceptable_types=args.types,
        acceptable_extensions=args.extensions,
        max_upload_file_size=args.max_size,
        file_mime_guessed_by_django=args.django_mime,
    )
    if args.max_size is not None:
        file_validator.validate_size()
    if args.types is not None:
        file_validator.validate_type()
    if args.extensions is not None:
        file_validator.validate_extension()
    if args.mimes is not None:
        _dispatch(file_validator, set_the_library(args.libraries))
    return file_validator.result_of_validation


def main(argv=None) -> int:
    """Validate a file and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if (
        args.mimes is None
        and args.types is None
        and args.extensions is None
        and args.max_size is None
    ):
        parser.error(
            "at least one of --mimes, --types, --extensions or --max-size "
            "is required"
        )

    try:
        result_of_validation = validate_file(args)
    except (
        FileValidationException,
        SizeValidationException,
        LibraryNotSupportedException,
        TypeNotSupportedException,
    ) as error:
        print(colored(str(error), "red"), file=sys.stderr)
        return 1

    print(colored("file is valid ✅", "green"))
    for library, result in result_of_validation.items():
        print(f"  {library}: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
