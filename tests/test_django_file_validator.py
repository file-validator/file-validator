"""Tests for DjangoFileValidator."""
import pytest
from django.core.exceptions import ValidationError
from django.db import models

from file_validator.constants import ALL
from file_validator.exceptions import (
    LibraryNotSupportedException,
    MimesEqualException,
    TypeNotSupportedException,
)
from file_validator.models import DjangoFileValidator

from tests.fixtures import (
    BAD_OBJECT,
    get_tmp_file,
    JPEG_FILE,
    JPEG_OBJECT,
    MIME,
    MP3_OBJECT,
    PNG_FILE,
    PNG_OBJECT,
)
from tests.project.app.models import (
    TestModelWithDjangoFileValidator,
    TestModelWithDjangoFileValidatorAndLibraryIsDjango,
    TestModelWithDjangoFileValidatorAndLibraryIsFiletype,
    TestModelWithDjangoFileValidatorAndLibraryIsMimetypes,
    TestModelWithDjangoFileValidatorAndLibraryIsNone,
    TestModelWithDjangoFileValidatorAndLibraryIsPureMagic,
    TestModelWithDjangoFileValidatorAndLibraryIsPythonMagic,
    TestModelWithDjangoFileValidatorAndSizeIsNone,
    TestModelWithDjangoFileValidatorWithAcceptableType,
)


class TestDjangoFileValidator:
    """Test DjangoFileValidator."""

    @staticmethod
    def test_django_file_validator_when_file_is_valid_and_return_none():
        """test when file is valid and return none."""
        new_instance = TestModelWithDjangoFileValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_file_is_not_valid_and_return_none():
        """test when file is not valid and return none."""
        with pytest.raises(ValidationError):
            new_instance = TestModelWithDjangoFileValidator(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT["name"],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT[MIME],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_file_size_is_none():
        """test when file size is none."""
        new_instance = TestModelWithDjangoFileValidatorAndSizeIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_libraries_is_none():
        """test when libraries is none."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_libraries_is_not_supported():
        """test when libraries is not supported."""
        with pytest.raises(LibraryNotSupportedException):

            class _TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                """Test Model."""

                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            acceptable_mimes=[PNG_OBJECT[MIME], MP3_OBJECT[MIME]],
                            libraries=[BAD_OBJECT["name"]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_acceptable_mimes_is_not_none_and_all_mimes_is_equal():
        """test when acceptable mimes is none."""
        with pytest.raises(MimesEqualException):

            class _TestFileModelWithDjangoFileValidatorAndNoneParameters(models.Model):
                """Test Model."""

                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            acceptable_mimes=[PNG_OBJECT[MIME], PNG_OBJECT[MIME]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_eq_methode():
        """test eq methode."""
        file_validator_one = DjangoFileValidator(
            acceptable_mimes=[PNG_OBJECT[MIME], MP3_OBJECT[MIME]],
            libraries=[ALL],
        )
        file_validator_two = DjangoFileValidator(
            acceptable_mimes=[PNG_OBJECT[MIME], MP3_OBJECT[MIME]],
            libraries=[ALL],
        )
        assert file_validator_one == file_validator_two

    @staticmethod
    def test_django_file_validator_hash_method():
        """Test for __hash__ method in FileValidator."""
        test_file = DjangoFileValidator(
            max_upload_file_size=1000,
            acceptable_mimes=[PNG_OBJECT[MIME]],
        )
        assert hash(test_file) == 1000

    @staticmethod
    def test_django_file_validator_acceptable_types_when_type_not_supported():
        """Test acceptable types in ValidatedFileField when the type not
        supported."""
        with pytest.raises(TypeNotSupportedException):

            class _TestModelWithDjangoFileValidatorAndBadAcceptableType(models.Model):
                """Test model class."""

                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            libraries=[ALL],
                            max_upload_file_size=1000000,
                            acceptable_types=[BAD_OBJECT["type"]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_when_library_is_python_magic():
        """Test django file validator when the library is python magic."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsPythonMagic(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_pure_magic():
        """Test django file validator when the library is pure magic."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsPureMagic(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_mimetypes():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsMimetypes(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_filetype():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsFiletype(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_django():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsDjango(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_acceptable_types_is_fill():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorWithAcceptableType(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()
