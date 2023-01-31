"""
This file is related to fixtures and constants required for tests
"""
import os

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile

from file_validator.models import ValidatedFileField

PNG_OBJECT: dict = {
    'name': 'test.png',
    'mime': 'image/png',
    'extension': 'png',
}

MP3_OBJECT: dict = {
    'name': 'test.mp3',
    'mime': 'audio/mpeg',
    'extension': 'mp3',
}

JPEG_OBJECT: dict = {
    'name': 'test.jpg',
    'mime': 'image/jpeg',
    'extension': 'jpg',
}

BAD_OBJECT: dict = {
    'name': 'bad.file',
    'mime': 'mime/bad',
    'extension': 'file',
}


TEMPLATE_EXPECTED_MESSAGE: str = "{file} : {mimes} with this {file_size} is not valid, you can upload files up to {max_file_size}"
EXPECTED_MESSAGE: str = "test.png : image/png, audio/mpeg with this 20 MB is not valid, you can upload files up to 10 MB"
TEST_LIBRARY: str = "test_library"


def get_test_file(file_name) -> str:
    """
    :param file_name: The name of the test file
    :return: It should return the path of the test file that is in the project
    """
    test_directory = os.path.dirname(os.path.realpath(__file__))
    test_files_directory = os.path.join(test_directory, "files", f"{file_name}")
    return test_files_directory


JPEG_FILE: str = get_test_file(JPEG_OBJECT['name'])
MP3_FILE: str = get_test_file(MP3_OBJECT['name'])
PNG_FILE: str = get_test_file(PNG_OBJECT['name'])
BAD_FILE: str = get_test_file(BAD_OBJECT['name'])


def get_tmp_file(file_name, file_path, file_mime_type):
    tmp_file = TemporaryUploadedFile(file_name, file_mime_type, 0, None)
    tmp_file.file = open(file_path)
    tmp_file.size = os.fstat(tmp_file.fileno()).st_size
    return tmp_file
