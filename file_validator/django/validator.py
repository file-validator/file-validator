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
class FileValidatorByPythonMagic:
    def __init__(self, *args):
        """
        :param args: You can choose different mime and pass it as a string and be sure to separate the types with commas, example: FileValidatorWithPythonMagic("image/png", "image/webp", "video/mp4")
        """
        if not all(args):
            error_message = """
                \n---------------------------------------------------------------
                \nThe args value is empty, please pass the value (file MIME).\nHow to fix this error? FileValidator("file MIME")\nYou can read the documentation for the full list of supported MIMES
                \n---------------------------------------------------------------
                """
            raise ValueError(colored(error_message, "red"))
        selected_mimes = []
        for mime in args:
            selected_mimes.append(mime)
        self.selected_mimes = selected_mimes

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        file_mime = magic.from_buffer(open(file_path, "rb").read(2048), mime=True)
        if file_mime not in self.selected_mimes:
            raise ValidationError(f"{file_mime} file is not valid")


@deconstructible
class FileValidatorByMimeTypes:
    def __init__(self, *args):
        self.selected_mimes = list(args)

    def __call__(self, value):
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        file_mime = guess_type(file_path)[0]
        if file_mime not in self.selected_mimes:
            raise ValidationError(f"{file_mime} it is unacceptable")


@deconstructible
class FileValidatorByFileType:
    """
    This file validation is done using the filetype library
    and mime and file extension are checked in this validation
    """

    def __init__(self, *args):
        """
        :param args: You can choose different types and pass it as a string and be sure to separate the types with commas, example: FileValidatorWithFileType("audio/mp3", "image/png")

        :raises ValueError: If the type you enter is not supported, it will cause this value error, please check that there are no typos, and you can check the list of supported types from the documentation.
        """
        if not all(args):
            error_message = """
            \n---------------------------------------------------------------
            \nThe args value is empty, please pass the value (file MIME).\nHow to fix this error? FileValidator("file mime, similar : image/png, audio/mp3")\nYou can read the documentation for the full list of supported types
            \n---------------------------------------------------------------
            """
            raise ValueError(colored(error_message, "red"))
        selected_mimes = []
        selected_extensions = []
        for selected_file_type in args:
            if is_mime_supported(selected_file_type):
                file_object = get_type(mime=selected_file_type)
                selected_mimes.append(file_object.MIME)
                selected_extensions.append(file_object.EXTENSION)
            else:
                error_message = f"""
                \n({selected_file_type}) Is Not Valid, Please Visit Documentation And Enter Valid Type\nHow to fix this error? FileValidator("file mime similar : image/png, audio/mp3")
                """
                raise ValueError(colored(error_message, "red"))
        self.selected_mimes = selected_mimes
        self.selected_extensions = selected_extensions

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        :return: If everything is ok, the permission to upload the file will be given, otherwise, a validation error will be returned
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        current_file = guess(file_path)
        if current_file.EXTENSION not in self.selected_extensions and current_file.MIME not in self.selected_mimes:
            raise ValidationError(f"{current_file.MIME} file is not valid")


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
