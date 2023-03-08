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
from tests.fixtures import BAD_OBJECT, MP3_OBJECT, PNG_OBJECT


class TestModelWithValidatedFileField(models.Model):
    """File Model With ValidatedFileField."""

    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldAndDjangoLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[DJANGO],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
        file_mime_guessed_by_django=PNG_OBJECT["mime"],
    )


class TestModelWithValidatedFileFieldAndFileTypeLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[FILETYPE],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldAndPureMagicLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PURE_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldAndMimetypesLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldAndPythonMagicLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldAndAllLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC, PURE_MAGIC, FILETYPE, MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class TestModelWithValidatedFileFieldWithoutLibrary(models.Model):
    test_file = ValidatedFileField(
        max_upload_file_size=1000000,
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
    )


class TestModelWithDjangoFileValidator(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[PYTHON_MAGIC],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                max_upload_file_size=10485760,
            ),
        ],
    )


class TestModelWithValidatedFileFieldWithAcceptableType(models.Model):
    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_types=[PNG_OBJECT["type"], MP3_OBJECT["type"]],
        max_upload_file_size=1000000,
    )


class TestModelWithFileSizeValidator(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=10485760,
            ),
        ],
    )


class TestModelWithDjangoFileValidatorAndBadAcceptableType(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[ALL],
                max_upload_file_size=1000000,
                acceptable_types=[BAD_OBJECT["type"]],
            ),
        ],
    )


class TestModelWithDjangoFileValidatorAndSizeIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[ALL],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class TestModelWithDjangoFileValidatorAndLibraryIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class TestModelWithFileSizeValidatorAndNotValidSize(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=100,
            ),
        ],
    )
