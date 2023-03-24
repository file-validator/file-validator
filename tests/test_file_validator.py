"""Module is related to tests."""
import os
from unittest import mock

import pytest

from file_validator.constants import AUDIO, FILETYPE, IMAGE, OK, VIDEO
from file_validator.exceptions import FileValidationException, TypeNotSupportedException
from file_validator.validators import FileValidator

from tests.fixtures import (
    BAD_FILE,
    EXTENSION,
    JPEG_FILE,
    JPEG_OBJECT,
    MAGIC_FILE,
    MIME,
    MP3_FILE,
    NAME,
    PNG_FILE,
    PNG_OBJECT,
    TYPE,
)


class TestFileValidatorByPythonMagic:
    """These tests are for file validators that are made using the python-magic
    library."""

    @staticmethod
    def test_file_validator_by_python_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """Test python_magic method library when file is valid."""
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT[MIME]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.python_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT[NAME]
        assert result_of_validation["file_mime"] == JPEG_OBJECT[MIME]
        assert result_of_validation["file_type"] == JPEG_OBJECT[TYPE]
        assert result_of_validation["file_extension"] == JPEG_OBJECT[EXTENSION]

    @staticmethod
    def test_file_validator_by_python_magic_library_when_file_is_not_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=jpeg,
            )
            file_validator.python_magic()

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_validator_by_python_magic_by_path_magic_file_from_env(
        self,
        jpeg=JPEG_FILE,
    ):
        """test file_validator_by_python_magic by path_magic file from .env
        file."""
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT[MIME]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.python_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT[NAME]
        assert result_of_validation["file_mime"] == JPEG_OBJECT[MIME]
        assert result_of_validation["file_type"] == JPEG_OBJECT[TYPE]
        assert result_of_validation["file_extension"] == JPEG_OBJECT[EXTENSION]


class TestFileValidatorByMimeTypes:
    """These tests are for file validators that are made using the mimetypes
    library."""

    @staticmethod
    def test_file_validator_by_mimetypes_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT[MIME]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.mimetypes()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT[NAME]
        assert result_of_validation["file_mime"] == JPEG_OBJECT[MIME]
        assert result_of_validation["file_type"] == JPEG_OBJECT[TYPE]
        assert result_of_validation["file_extension"] == JPEG_OBJECT[EXTENSION]

    @staticmethod
    def test_file_validator_by_mimetypes_library_when_file_is_not_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=jpeg,
            )
            file_validator.mimetypes()

    @staticmethod
    def test_mimetypes_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=BAD_FILE,
            )
            file_validator.mimetypes()


class TestFileValidatorByPureMagic:
    """These tests are for file validators that are made using the filetype
    library."""

    @staticmethod
    def test_file_validator_by_pure_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """Test file_validator_by_pure_magic the library when file is valid."""
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT[MIME]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.pure_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT[NAME]
        assert result_of_validation["file_mime"] == JPEG_OBJECT[MIME]
        assert result_of_validation["file_type"] == JPEG_OBJECT[TYPE]
        assert result_of_validation["file_extension"] == JPEG_OBJECT[EXTENSION]

    @staticmethod
    def test_file_validator_by_pure_magic_library_when_file_is_not_valid():
        """Test file_validator_by_pure_magic the library when file is not
        valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[JPEG_OBJECT[MIME]],
                file_path=PNG_FILE,
            )
            file_validator.pure_magic()

    @staticmethod
    def test_pure_magic_library_when_it_could_not_detect_the_mime_file():
        """Test the pure_magic library when it could not detect the mime
        file."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=BAD_FILE,
            )
            file_validator.pure_magic()


class TestFileValidatorByFileType:
    """These tests are for file validators that are made using the filetype
    library."""

    @staticmethod
    def test_file_validator_by_filetype_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """Test file_validator_by_filetype the library when file is valid."""
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT[MIME]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.filetype()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT[NAME]
        assert result_of_validation["file_mime"] == JPEG_OBJECT[MIME]
        assert result_of_validation["file_type"] == JPEG_OBJECT[TYPE]
        assert result_of_validation["file_extension"] == JPEG_OBJECT[EXTENSION]

    @staticmethod
    def test_file_validator_by_filetype_library_when_file_is_not_valid(
        mp3_file=MP3_FILE,
    ):
        """Test file_validator_by_filetype the library when file is not
        valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[JPEG_OBJECT[MIME]],
                file_path=mp3_file,
            )
            file_validator.filetype()

    @staticmethod
    def test_filetype_library_when_it_could_not_detect_the_mime_file():
        """Test filetype library when it could not detect the mime file."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=BAD_FILE,
            )
            file_validator.filetype()


class TestFileExtensionValidator:
    """Test validate_extension method."""

    @staticmethod
    def test_file_extension_validator_when_file_is_valid():
        """Test file extension validator when file is valid."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_extensions=[PNG_OBJECT[EXTENSION]],
        )
        file_validator.validate_extension()

    @staticmethod
    def test_file_extension_validator_when_file_is_not_valid():
        """Test file extension validator when file is not valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_path=PNG_FILE,
                acceptable_extensions=[JPEG_OBJECT[EXTENSION]],
            )
            file_validator.validate_extension()


class TestFileValidatorByType:
    """tests for file_validator_by_type function."""

    @staticmethod
    def test_file_validator_by_type_when_type_is_not_supported():
        """test for file_validator_by_type when type is not supported."""
        with pytest.raises(TypeNotSupportedException):
            file_validator = FileValidator(
                acceptable_types=["test_type"],
                file_path=PNG_FILE,
            )
            file_validator.validate_type()

    @staticmethod
    def test_file_validator_by_type_when_return_file_validation_exception():
        """test for file_validator_by_type when return file validation
        exception."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_types=[VIDEO, AUDIO],
                file_path=PNG_FILE,
            )
            file_validator.validate_type()

    @staticmethod
    def test_file_validator_by_type_when_return_validation_data_and_file_is_valid():
        """test for file_validator_by_type when return validation data and file
        is valid."""
        file_validator = FileValidator(
            acceptable_types=[IMAGE, AUDIO],
            file_path=PNG_FILE,
        )
        result_of_validation = file_validator.validate_type()
        assert result_of_validation["status"] == OK
        assert result_of_validation["library"] == FILETYPE
        assert result_of_validation["file_name"] == PNG_OBJECT[NAME]


class TestFileValidatorDjango:
    """Test django method FileValidator."""

    @staticmethod
    def test_file_validation_by_django_data_when_file_is_not_valid():
        """Test FileValidator when the library is django and file is not
        valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_mime_guessed_by_django=JPEG_OBJECT[MIME],
                acceptable_mimes=[PNG_OBJECT[MIME]],
                file_path=JPEG_FILE,
            )
            file_validator.django()

    @staticmethod
    def test_validate_method_when_file_mime_guessed_parameter_by_django_is_not_fill():
        """Test validate method when file_mime_guessed parameter by django is
        not fill."""
        file_validator = FileValidator(
            acceptable_mimes=[PNG_OBJECT[MIME]],
            file_path=PNG_FILE,
        )
        file_validator.validate()


class TestFileMimeValidator:
    """Test validate_mime method."""

    @staticmethod
    def test_file_mime_validation_when_mime_file_is_valid():
        """Test file mime validation when mime file is valid."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_mimes=[PNG_OBJECT[MIME]],
        )
        file_validator.validate_mime()

    @staticmethod
    def test_file_mime_validation_when_mime_file_is_not_valid():
        """Test file mime validation when mime file is not valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_path=PNG_FILE,
                acceptable_mimes=[JPEG_OBJECT[MIME]],
            )
            file_validator.validate_mime()

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_mime_validation_by_path_magic_file_from_env(
        self,
    ):
        """Test file mime validation by path magic file from env file."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_mimes=[PNG_OBJECT[MIME]],
        )
        file_validator.validate_mime()
