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
class FileValidatorWithFileType:
    """
    This file validation is done using the filetype library
    and mime and file extension are checked in this validation
    """

    def __init__(self, *args):
        """
        :param args: You can choose different types and pass it as a string and be sure to separate the types with commas, example: FileValidatorWithFileType("mp3", "avi")

        :raises ValueError: If the type you enter is not supported, it will cause this value error, please check that there are no typos, and you can check the list of supported types from the documentation.
        """
        if not all(args):
            error_message = """
            \n---------------------------------------------------------------
            \nThe args value is empty, please pass the value (file extension).\nHow to fix this error? FileValidator("file type or extension")\nYou can read the documentation for the full list of supported types
            \n---------------------------------------------------------------
            """
            raise ValueError(colored(error_message, "red"))
        selected_types = {}
        for selected_file_type in args:
            if is_extension_supported(selected_file_type):
                file_object = get_type(ext=selected_file_type)
                selected_types.update(
                    {
                        selected_file_type: file_object,
                    }
                )
            else:
                error_message = f"""
                \n({selected_file_type}) Is Not Valid, Please Visit Documentation And Enter Valid Type\nHow to fix this error? FileValidator("file type or extension")
                """
                raise ValueError(colored(error_message, "red"))
        self.selected_types = selected_types

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        :return: If everything is ok, the permission to upload the file will be given, otherwise, a validation error will be returned
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        result_validation = []
        current_file = guess(file_path)
        """
        Here, if we cannot detect the upload file type using
        the filetype library, we will create a validation error.
        """
        if current_file is not None:
            for file_extension, file_object in self.selected_types.items():
                if (
                    current_file.EXTENSION != file_extension
                    and current_file.MIME != file_object.MIME
                ):
                    result_validation.append(True)
                elif (
                    current_file.EXTENSION == file_extension
                    and current_file.MIME == file_object.MIME
                ):
                    result_validation.append(False)
        else:
            raise ValidationError("Please Upload a Valid File")
        """
        Here we compare the file with all the types we have determined
        If the type and extension of the files do not match what we had
        in the model, we will return the True value, otherwise, if both
        the value and the type are equal to one of the types we specified,
        it will return the False value, and if the result The validation of
        each file is returned to True, so here we can understand that this
        file does not match any of the types of files that we specified, and
        using the all() function, we AND (&) the True values in result_validation
        together. and show a validation error, otherwise, if only one returns False,
        then the file has been successfully validated.
        """
        file_is_not_valid = all(result_validation)
        if file_is_not_valid:
            raise ValidationError(
                f"{current_file.extension} File Is Not Valid, Please Upload a valid Type"
            )


@deconstructible
class FileValidatorWithPythonMagic:
    def __init__(self, *args):
        """
        :param args:  You can choose different mime and pass it as a string and be sure to separate the types with commas, example: FileValidatorWithPythonMagic("image/png", "image/webp", "video/mp4")
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
class FileValidatorWithMimeTypes:
    def __init__(self, *args):
        self.selected_mimes = list(args)

    def __call__(self, value):
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        file_mime = guess_type(file_path)[0]
        if file_mime not in self.selected_mimes:
            raise ValidationError(f"{file_mime} it is unacceptable")


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
