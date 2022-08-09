import os
import pytest


def get_test_file(file_name):
    test_directory = os.path.dirname(os.path.realpath(__file__))
    test_files_directory = os.path.join(test_directory, "test_files", f"{file_name}")
    return test_files_directory


@pytest.fixture
def jpeg_file():
    file = get_test_file(file_name="test.jpg")
    return file


@pytest.fixture
def mp3_file():
    file = get_test_file(file_name="test.mp3")
    return file


@pytest.fixture
def text_file():
    file = get_test_file(file_name="test.txt")
    return file


BAD_MIME = "mime/bad"
JPEG_MIME = "image/jpeg"
MP3_MIME = "audio/mpeg"
JPEG_EXTENSION = "jpg"
MP3_EXTENSION = "mp3"
