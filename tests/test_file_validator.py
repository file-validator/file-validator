"""
This module is related to tests
"""
from file_validator.file_validator.validator import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
)
from .fixtures import MP3_MIME, JPEG_MIME, PNG_MIME, JPEG_FILE, MP3_FILE, PNG_FILE
from file_validator.django_example.post.models import ValidFile
from ..file_validator.exceptions import error_message


class TestFileValidatorByPythonMagic:
    """
    These tests are for file validators that are made using the python-magic library
    """

    def test_file_validator_when_file_is_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_python_magic(JPEG_MIME, file_path=jpeg) is None

    def test_file_validator_when_file_is_not_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        try:
            file_validator_by_python_magic(PNG_MIME, file_path=jpeg)
        except ValueError as error:
            assert JPEG_MIME in str(error)

    # def test_file_validator_when_file_is_not_valid_and_raise_attribute_error(self):
    #     pass

    def test_file_validator_when_file_is_valid_in_django(
        self, jpeg=JPEG_FILE, file=ValidFile
    ):
        new_file = file(file=jpeg)
        new_file.full_clean()


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


def test_error_message_function_return_correct_message():
    """
    We test whether this error message function returns the expected message or not
    """
    message = error_message(
        message="{file} : {mimes} with this {file_size} is not valid,  you can upload files up to {max_file_size}",
        file="test.png",
        file_size="20 MB",
        mimes=["image/png", "audio/mpeg"],
        max_file_size="10 MB",
    )
    expected_message = "test.png : image/png, audio/mpeg with this 20 MB is not valid,  you can upload files up to 10 MB"
    assert expected_message in message
