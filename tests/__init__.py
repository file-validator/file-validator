"""Unit test package for file_validator."""
from file_validator.file_validator.validators import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
)
from .fixtures import MP3_MIME, JPEG_MIME, PNG_MIME, JPEG_FILE, MP3_FILE
