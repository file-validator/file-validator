import pytest
from file_validator import file_validator
import os
import magic
from file_validator.file_validator.validator import (
    get_mime_by_python_magic,
    get_mime_by_filetype,
    get_mime_by_mimetypes,
    get_extension_by_filetype,
    file_validation_by_filetype,
    file_validation_by_python_magic,
    file_validation_by_mimetypes,
    file_validation
)
from filetype import guess, is_mime_supported, is_extension_supported
from .fixtures import (
    MP3_EXTENSION,
    MP3_MIME,
    JPEG_EXTENSION,
    JPEG_MIME,
    BAD_MIME,
    jpeg_file,
    mp3_file,
    text_file,
    PNG_MIME,
)


class TestFileValidationByPythonMagic:
    def test_get_mime_by_python_magic_return_correct_mime(self, jpeg_file):
        file_mime = get_mime_by_python_magic(jpeg_file)
        assert file_mime == JPEG_MIME

    def test_file_validation_by_python_magic_library_when_file_is_valid(
        self, jpeg_file
    ):
        result_of_validation = file_validation_by_python_magic(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validation_by_python_magic_library_when_file_is_not_valid(
        self, jpeg_file
    ):
        try:
            file_validation_by_python_magic(PNG_MIME, file_path=jpeg_file)
        except ValueError as error:
            assert JPEG_MIME in str(error)


class TestFileValidationByFileType:
    def test_get_mime_by_filetype_return_correct_mime(self, jpeg_file):
        file_mime = get_mime_by_filetype(jpeg_file)
        assert file_mime == JPEG_MIME

    def test_get_extension_by_filetype_return_correct_extension(self, jpeg_file):
        file_extension = get_extension_by_filetype(jpeg_file)
        assert file_extension == JPEG_EXTENSION

    def test_file_validation_by_filetype_library_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validation_by_filetype(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validation_by_filetype_library_when_file_is_not_valid(self, mp3_file):
        try:
            file_validation_by_filetype(JPEG_MIME, file_path=mp3_file)
        except ValueError as error:
            assert MP3_MIME in str(error)


class TestFileValidationByMimeTypes:
    def test_get_mime_by_mimetypes_return_correct_mime(self, jpeg_file):
        file_mime = get_mime_by_mimetypes(jpeg_file)
        assert file_mime == JPEG_MIME

    def test_file_validation_by_mimetypes_library_when_file_is_valid(self, jpeg_file):
        result_of_validation = file_validation_by_mimetypes(
            JPEG_MIME, file_path=jpeg_file
        )
        assert result_of_validation is None

    def test_file_validation_by_mimetypes_library_when_file_is_not_valid(
        self, jpeg_file
    ):
        try:
            file_validation_by_mimetypes(PNG_MIME, file_path=jpeg_file)
        except ValueError as error:
            assert JPEG_MIME in str(error)


def test_file_validation_when_file_is_valid(jpeg_file):
    result_of_validation = file_validation(JPEG_MIME, file_path=jpeg_file)
    assert result_of_validation is None


def test_file_validation_when_file_is_not_valid(jpeg_file):
    try:
        file_validation(PNG_MIME, file_path=jpeg_file)
    except ValueError as error:
        assert JPEG_MIME in str(error)
