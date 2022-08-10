from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from filetype import get_type, is_mime_supported, guess
from termcolor import colored


@deconstructible
class FileValidator:
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
            \nThe args value is empty, please pass the value (file mime).\nHow to fix this error? FileValidator("file mime, similar : image/png, audio/mp3")\nYou can read the documentation for the full list of supported types
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
