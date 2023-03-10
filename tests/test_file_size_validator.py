"""Tests for FileSizeValidator."""
import pytest
from django.core.exceptions import ValidationError
from django.db import models

from file_validator.exceptions import SizeValidationException
from file_validator.models import FileSizeValidator
from file_validator.validators import FileValidator

from tests.fixtures import get_tmp_file, PNG_FILE, PNG_OBJECT
from tests.project.app.models import (
    TestModelWithFileSizeValidator,
    TestModelWithFileSizeValidatorAndNotValidSize,
)


class TestFileSizeValidator:
    """test file size validator."""

    @staticmethod
    def test_file_size_is_valid():
        """test file size is valid."""
        new_instance = TestModelWithFileSizeValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_file_size_is_not_valid():
        """test file size is not valid."""
        with pytest.raises(ValidationError):
            new_instance = TestModelWithFileSizeValidatorAndNotValidSize(
                test_file=get_tmp_file(
                    file_name=PNG_OBJECT["name"],
                    file_path=PNG_FILE,
                    file_mime_type=PNG_OBJECT["mime"],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_max_upload_file_size_is_none():
        """test max upload file size is none."""
        with pytest.raises(SizeValidationException):

            class _TestFileModelWithFileValidatorNotMaxUploadSize(models.Model):
                test_file = models.FileField(validators=[FileSizeValidator()])

    @staticmethod
    def test_eq_method():
        """test eq method."""
        file_validator_one = FileSizeValidator(max_upload_file_size=10485760)
        file_validator_two = FileSizeValidator(max_upload_file_size=10485760)
        assert file_validator_one == file_validator_two

    @staticmethod
    def test_hash_method():
        """Test for __hash__ method in FileSizeValidator."""
        test_file = FileSizeValidator(
            max_upload_file_size=1000,
        )
        assert hash(test_file) == 1000

    @staticmethod
    def test_size_validator():
        """Test validate_size method FileValidator."""
        with pytest.raises(SizeValidationException):
            file_validator = FileValidator(max_upload_file_size=1, file_path=PNG_FILE)
            file_validator.validate_size()
