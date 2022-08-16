"""Top-level package for File Validator."""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from filetype import get_type, guess, is_mime_supported
from termcolor import colored
from file_validator.file_validator import exceptions
from file_validator.file_validator import validator
from file_validator.file_validator import django

__author__ = """Reza Shakeri"""
__email__ = 'rzashakeri@outlook.com'
__version__ = '0.1.4'
