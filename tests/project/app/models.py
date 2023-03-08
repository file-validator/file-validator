from django.db import models

from file_validator.constants import (
    ALL,
    DJANGO,
    FILETYPE,
    MIMETYPES,
    PURE_MAGIC,
    PYTHON_MAGIC,
)
from file_validator.models import (
    DjangoFileValidator,
    FileSizeValidator,
    ValidatedFileField,
)
from tests.fixtures import MP3_OBJECT, PNG_OBJECT


class FileModel(models.Model):
    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithAllLibraries(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC, PURE_MAGIC, FILETYPE, MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithDjango(models.Model):
    test_file = ValidatedFileField(
        libraries=[DJANGO],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
        file_mime_guessed_by_django=PNG_OBJECT["mime"],
    )


class FileModelWithFileType(models.Model):
    test_file = ValidatedFileField(
        libraries=[FILETYPE],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithPureMagic(models.Model):
    test_file = ValidatedFileField(
        libraries=[PURE_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithMimetypes(models.Model):
    test_file = ValidatedFileField(
        libraries=[MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithPythonMagic(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class FileModelWithoutLibraries(models.Model):
    test_file = ValidatedFileField(
        max_upload_file_size=1000000,
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
    )


class FileModelWithFileValidator(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[PYTHON_MAGIC],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                max_upload_file_size=10485760,
            ),
        ],
    )


class FileModelWithAcceptableType(models.Model):
    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_types=[PNG_OBJECT["type"], MP3_OBJECT["type"]],
        max_upload_file_size=1000000,
    )


class FileModelWithFileSizeValidator(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=10485760,
            ),
        ],
    )


class FileModelWithFileValidatorSizeIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[ALL],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class FileModelWithFileValidatorLibraryIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class FileModelWithFileSizeValidatorNotValidSize(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=100,
            ),
        ],
    )
