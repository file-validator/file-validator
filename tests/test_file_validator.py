"""
This module is related to tests
"""
from file_validator.file_validator.validator import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
)
from .fixtures import MP3_MIME, JPEG_MIME, PNG_MIME, JPEG_FILE, MP3_FILE


class TestFileValidatorByPythonMagic:
    """
    These tests are for file validators that are made using the python-magic library
    """

    def test_file_validator_by_python_magic_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_python_magic(JPEG_MIME, file_path=jpeg) is None

    def test_file_validator_by_python_magic_library_when_file_is_not_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        try:
            file_validator_by_python_magic(PNG_MIME, file_path=jpeg)
        except ValueError as error:
            assert JPEG_MIME in str(error)


class TestFileValidatorByMimeTypes:
    """
    These tests are for file validators that are made using the mimetypes library
    """

    def test_file_validator_by_mimetypes_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_mimetypes(JPEG_MIME, file_path=jpeg) is None

    def test_file_validator_by_mimetypes_library_when_file_is_not_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        try:
            file_validator_by_mimetypes(PNG_MIME, file_path=jpeg)
        except ValueError as error:
            assert JPEG_MIME in str(error)


class TestFileValidatorByFileType:
    """
    These tests are for file validators that are made using the filetype library
    """

    def test_file_validator_by_filetype_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_filetype(JPEG_MIME, file_path=jpeg) is None

    def test_file_validator_by_filetype_library_when_file_is_not_valid(
        self, mp3_file=MP3_FILE
    ):
        """
        :param mp3_file: It is a fixture for mp3 files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        try:
            file_validator_by_filetype(JPEG_MIME, file_path=mp3_file)
        except ValueError as error:
            assert MP3_MIME in str(error)


class TestFileValidator:
    """
    These tests are for file validators that are made using the filetype library
    """

    def test_file_validator_when_file_is_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator(JPEG_MIME, file_path=jpeg) is None

    def test_file_validation_when_file_is_not_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        try:
            file_validator(PNG_MIME, file_path=jpeg)
        except ValueError as error:
            assert JPEG_MIME in str(error)
