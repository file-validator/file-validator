from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.conf import settings
from filetype import get_type, is_extension_supported, is_mime_supported, guess
from termcolor import colored
import magic
from mimetypes import guess_type, guess_extension


@deconstructible
class FileValidator:
    def __init__(self, *args, python_magic=False):
        """
        :param args: You can choose different mime and pass it as a string and be sure to separate the types with commas, example : FileValidator("image/png", "image/webp", "video/mp4")
        :param python_magic: Since the python magic library may treat audio files like mp3 as programs or octal streams and it's a bit annoying, the default value of the python_magic parameter is set to false, but if you still want to use the python magic library , you can set this option to True to have the Python magic library perform validation in addition to the filetype and mimetypes libraries.
        """
        selected_mimes = []
        for mime in args:
            if is_mime_supported(mime):
                file_object = get_type(mime=mime)
                selected_mimes.append(file_object.MIME)
            else:
                error_message = f"""
                ----------------------------------------------------------------------
                => {mime} is not supported, Read the documentation for supported mimes
                ----------------------------------------------------------------------
                """
                raise ValueError(colored(error_message, "red"))
        self.selected_mimes = selected_mimes
        self.must_be_validated_by_Python_magic: bool = python_magic

    def __call__(self, value):
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        file_mime_with_python_magic = magic.from_buffer(
            open(file_path, "rb").read(2048), mime=True
        )  # get file mime use python magic library
        file_mime_with_filetype_lib = guess(
            file_path
        ).MIME  # get file mime use filetype library
        file_mime_with_mimetypes_lib = guess_type(file_path)[
            0
        ]  # get the file mime use mimetypes library (native in python)
        if self.must_be_validated_by_Python_magic:
            if (
                file_mime_with_filetype_lib
                and file_mime_with_mimetypes_lib
                and file_mime_with_python_magic not in self.selected_mimes
            ):
                raise ValidationError(f"{file_mime_with_python_magic} is not valid")
        else:
            if (
                file_mime_with_filetype_lib not in self.selected_mimes
                or file_mime_with_mimetypes_lib not in self.selected_mimes
            ):
                raise ValidationError(f"{file_mime_with_filetype_lib} is not valid")
