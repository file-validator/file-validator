"""This file is related to fixtures and constants required for tests."""
import os

from django.core.files.uploadedfile import TemporaryUploadedFile

MIME: str = "mime"
NAME: str = "name"
TYPE: str = "type"
EXTENSION: str = "extension"

PNG_OBJECT: dict = {
    NAME: "test.png",
    MIME: "image/png",
    TYPE: "image",
    EXTENSION: ".png",
}

MP3_OBJECT: dict = {
    NAME: "test.mp3",
    MIME: "audio/mpeg",
    TYPE: "audio",
    EXTENSION: ".mp3",
}

MP4_OBJECT: dict = {
    NAME: "test.mp4",
    MIME: "video/mp4",
    TYPE: "video",
    EXTENSION: ".mp4",
}

JPEG_OBJECT: dict = {
    NAME: "test.jpg",
    MIME: "image/jpeg",
    TYPE: "image",
    EXTENSION: ".jpg",
}

ZIP_OBJECT: dict = {
    NAME: "test.zip",
    MIME: "application/zip",
    TYPE: "application",
    EXTENSION: ".zip",
}

TTF_OBJECT: dict = {
    NAME: "test.ttf",
    MIME: "application/font-sfnt",
    TYPE: "application",
    EXTENSION: ".ttf",
}

BAD_OBJECT: dict = {
    NAME: "bad.file",
    MIME: "mime/bad",
    TYPE: "bad",
    EXTENSION: ".file",
}


TEMPLATE_EXPECTED_MESSAGE: str = "{current_file_name} {current_file_mime} {acceptable_mimes} {current_file_size} {max_file_size}"
EXPECTED_MESSAGE: str = "test.png image/png image/png, audio/mpeg 20 MB 10 MB"
TEST_LIBRARY: str = "test_library"


def get_test_file(file_name) -> str:
    """
    :param file_name: The name of the test file
    :return: It should return the path of the test file that is in the project
    """
    test_directory = os.path.dirname(os.path.realpath(__file__))
    test_files_directory = os.path.join(test_directory, "files", file_name)
    return test_files_directory


MAGIC_FILE: str = get_test_file("magic.mgc")
JPEG_FILE: str = get_test_file(JPEG_OBJECT[NAME])
MP3_FILE: str = get_test_file(MP3_OBJECT[NAME])
MP4_FILE: str = get_test_file(MP4_OBJECT[NAME])
PNG_FILE: str = get_test_file(PNG_OBJECT[NAME])
ZIP_FILE: str = get_test_file(ZIP_OBJECT[NAME])
TTF_FILE: str = get_test_file(TTF_OBJECT[NAME])
BAD_FILE: str = get_test_file(BAD_OBJECT[NAME])


def get_tmp_file(file_name, file_path, file_mime_type):
    """
    :param file_name: The name of the test file
    :param file_path: The path of the test file
    :param file_mime_type: The mime of the test file
    """
    tmp_file = TemporaryUploadedFile(file_name, file_mime_type, 0, None)
    with open(file_path, encoding="utf-8") as file:
        tmp_file.file = file
        tmp_file.size = os.fstat(tmp_file.fileno()).st_size
        return tmp_file
