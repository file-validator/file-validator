from django.db import models

from file_validator.constants import ALL, PYTHON_MAGIC
from file_validator.models import FileSizeValidator, FileValidator, ValidatedFileField
from tests.fixtures import MP3_OBJECT, PNG_OBJECT


class TestFileModel(models.Model):
    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestFileModelWithoutLibraries(models.Model):
    test_file = ValidatedFileField(
        max_upload_file_size=1000000,
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
    )


class TestFileModelWithFileValidator(models.Model):
    test_file = models.FileField(
        validators=[
            FileValidator(
                libraries=[PYTHON_MAGIC],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                max_upload_file_size=10485760,
            ),
        ],
    )


class TestFileModelWithFileSizeValidator(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=10485760,
            ),
        ],
    )


class TestFileModelWithFileValidatorSizeIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            FileValidator(
                libraries=[ALL],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class TestFileModelWithFileValidatorLibraryIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class TestFileModelWithFileSizeValidatorNotValidSize(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=100,
            ),
        ],
    )
