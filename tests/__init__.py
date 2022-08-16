"""Unit test package for file_validator."""
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'file_validator.django_example.django_example.settings'
django.setup()

from file_validator.file_validator.validator import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
)
from .fixtures import MP3_MIME, JPEG_MIME, PNG_MIME, JPEG_FILE, MP3_FILE
