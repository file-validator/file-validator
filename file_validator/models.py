"""
test
"""

from django.db.models import FileField
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from termcolor import colored

from file_validator.file_validator.exceptions import error_message
from file_validator.file_validator.validators import size_validator, file_validator_by_django
from file_validator.file_validator.constants import MIMES_EMPTY


class ValidatedFileField(FileField):
    """
    :type
    """
    def __init__(self, **kwargs):
        self.acceptable_mimes: list = kwargs.get('acceptable_mimes')
        if self.acceptable_mimes is None or not all(self.acceptable_mimes):
            raise ValueError(colored(MIMES_EMPTY, "red"))
        self.libraries: list = kwargs.get('libraries')
        self.max_upload_file_size: int = kwargs.get('max_upload_file_size')
        super().__init__()

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        file = data.file
        content_type_guessed_by_django = file.content_type
        file_size = file.size
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        size_validator(
            max_upload_file_size=self.max_upload_file_size,
            acceptable_mimes=self.acceptable_mimes,
            file_size=file_size,
            file=file
        )
        try:
            file_validator_by_django(
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                file_path=file_path,
                content_type_guessed_by_django=content_type_guessed_by_django
            )

        except ValueError as error:
            raise ValidationError(
                error_message(
                    file=file,
                    file_size=filesizeformat(file_size),
                    max_file_size=filesizeformat(self.max_upload_file_size),
                    mimes=self.acceptable_mimes,
                )
            ) from error

        return data
