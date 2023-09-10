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


# ValidatedFileField
class ModelWithValidatedFileField(models.Model):
    """File Model With ValidatedFileField."""

    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndDjangoLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[DJANGO],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndFileTypeLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[FILETYPE],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndPureMagicLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PURE_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndMimetypesLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndPythonMagicLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldAndAllLibrary(models.Model):
    test_file = ValidatedFileField(
        libraries=[PYTHON_MAGIC, PURE_MAGIC, FILETYPE, MIMETYPES],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldWithoutLibrary(models.Model):
    test_file = ValidatedFileField(
        max_upload_file_size=1000000,
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
    )


class ModelWithValidatedFileFieldWithAcceptableType(models.Model):
    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_types=[PNG_OBJECT["type"], MP3_OBJECT["type"]],
        max_upload_file_size=1000000,
    )


class ModelWithValidatedFileFieldWithoutMaxUploadFileSize(models.Model):
    """File Model With ValidatedFileField."""

    test_file = ValidatedFileField(
        libraries=["all"],
        acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
    )


# DjangoFileValidator
class ModelWithDjangoFileValidator(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[PYTHON_MAGIC],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                max_upload_file_size=10485760,
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndSizeIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                libraries=[ALL],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsNone(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsPythonMagic(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[PYTHON_MAGIC],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsPureMagic(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[PURE_MAGIC],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsMimetypes(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[MIMETYPES],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsFiletype(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[FILETYPE],
            ),
        ],
    )


class ModelWithDjangoFileValidatorAndLibraryIsDjango(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[DJANGO],
            ),
        ],
    )


class ModelWithDjangoFileValidatorWithAcceptableType(models.Model):
    test_file = models.FileField(
        validators=[
            DjangoFileValidator(
                acceptable_types=[PNG_OBJECT["type"], MP3_OBJECT["type"]],
            ),
        ],
    )


# FileSizeValidator
class ModelWithFileSizeValidator(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=10485760,
            ),
        ],
    )


class ModelWithFileSizeValidatorAndNotValidSize(models.Model):
    test_file = models.FileField(
        validators=[
            FileSizeValidator(
                max_upload_file_size=100,
            ),
        ],
    )
