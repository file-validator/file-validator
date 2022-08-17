"""Top-level package for File Validator."""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from filetype import get_type, guess, is_mime_supported
from termcolor import colored
from . import exceptions
from . import validator
from . import django

__author__ = """Reza Shakeri"""
__email__ = 'rzashakeri@outlook.com'
__version__ = '0.1.5'
