from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from termcolor import colored
from mimetypes import guess_type


@deconstructible
class FileValidator:
    def __init__(self, *args):
        self.selected_mimes = list(args)

    def __call__(self, value):
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        file_mime = guess_type(file_path)[0]
        if file_mime not in self.selected_mimes:
            raise ValidationError(f"{file_mime} it is unacceptable")
