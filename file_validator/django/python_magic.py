from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from termcolor import colored
import magic


@deconstructible
class FileValidator:
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
