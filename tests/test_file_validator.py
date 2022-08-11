from .fixtures import (
    MP3_MIME,
    JPEG_MIME,
    PNG_MIME,
    jpeg_file,
    mp3_file
)
from file_validator.file_validator.validator import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator
)


class TestFileValidatorByPythonMagic:
    def test_file_validator_by_python_magic_library_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validator_by_python_magic(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validator_by_python_magic_library_when_file_is_not_valid(
        self, jpeg_file
    ):
        try:
            file_validator_by_python_magic(PNG_MIME, file_path=jpeg_file)
        except ValueError as error:
            assert JPEG_MIME in str(error)


class TestFileValidatorByMimeTypes:
    def test_file_validator_by_mimetypes_library_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validator_by_mimetypes(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validator_by_mimetypes_library_when_file_is_not_valid(
        self, jpeg_file
    ):
        try:
            file_validator_by_mimetypes(PNG_MIME, file_path=jpeg_file)
        except ValueError as error:
            assert JPEG_MIME in str(error)


class TestFileValidatorByFileType:
    def test_file_validator_by_filetype_library_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validator_by_filetype(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validator_by_filetype_library_when_file_is_not_valid(self, mp3_file):
        try:
            file_validator_by_filetype(JPEG_MIME, file_path=mp3_file)
        except ValueError as error:
            assert MP3_MIME in str(error)


class TestFileValidator:

    def test_file_validator_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validator(JPEG_MIME, file_path=jpeg_file)
        assert result_of_validation is None

    def test_file_validation_when_file_is_not_valid(self, jpeg_file):
        try:
            file_validator(PNG_MIME, file_path=jpeg_file)
        except ValueError as error:
            assert JPEG_MIME in str(error)
