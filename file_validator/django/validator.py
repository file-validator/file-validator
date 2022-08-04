from .file_types import FILE_TYPES
from django.core import validators
from django.core.exceptions import ValidationError
import filetype
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator:
    def __init__(self, *args):
        """

        :param args: You can choose different types and pass it
        as a string and be sure to separate the types with commas
        :type str
        => example : FileValidator("mp3", "avi")

        """
        selected_types = {}
        for selected_file_type in args:
            if selected_file_type in FILE_TYPES.keys():
                selected_types.update({selected_file_type:FILE_TYPES[selected_file_type]})
                print(selected_types)
            else:
                raise ValueError(f"{selected_file_type} Is Not Valid, Please Visit Documentation And Enter Valid Type")


    def __call__(self, value):
        pass

