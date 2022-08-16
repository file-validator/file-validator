"""
This file is related to fixtures and constants required for tests
"""
import os

BAD_MIME = "mime/bad"
JPEG_MIME = "image/jpeg"
MP3_MIME = "audio/mpeg"
PNG_MIME = "image/png"

JPEG_EXTENSION = "jpg"
MP3_EXTENSION = "mp3"
PNG_EXTENSION = "png"


def get_test_file(file_name):
    """
    :param file_name: The name of the test file
    :return: It should return the path of the test file that is in the project
    """
    test_directory = os.path.dirname(os.path.realpath(__file__))
    test_files_directory = os.path.join(test_directory, "test_files", f"{file_name}")
    return test_files_directory


JPEG_FILE = get_test_file("test.jpg")
MP3_FILE = get_test_file("test.mp3")
PNG_FILE = get_test_file("test.png")
BAD_FILE = get_test_file("test.bad")
