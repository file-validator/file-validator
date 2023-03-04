"""This file is related to fixtures and constants required for tests."""
import os

from django.core.files.uploadedfile import TemporaryUploadedFile

PNG_OBJECT: dict = {
    "name": "test.png",
    "mime": "image/png",
    "type": "image",
    "extension": ".png",
}

MP3_OBJECT: dict = {
    "name": "test.mp3",
    "mime": "audio/mpeg",
    "type": "audio",
    "extension": ".mp3",
}

MP4_OBJECT: dict = {
    "name": "test.mp4",
    "mime": "video/mp4",
    "type": "video",
    "extension": ".mp4",
}

JPEG_OBJECT: dict = {
    "name": "test.jpg",
    "mime": "image/jpeg",
    "type": "image",
    "extension": ".jpg",
}

ZIP_OBJECT: dict = {
    "name": "test.zip",
    "mime": "application/zip",
    "type": "application",
    "extension": ".zip",
}

TTF_OBJECT: dict = {
    "name": "test.ttf",
    "mime": "application/font-sfnt",
    "type": "application",
    "extension": ".ttf",
}

BAD_OBJECT: dict = {
    "name": "bad.file",
    "mime": "mime/bad",
    "type": "bad",
    "extension": ".file",
}

TEMPLATE_EXPECTED_MESSAGE: str = (
    "{file_name} {current_file_mime} {mimes} {file_size} {max_file_size}"
)
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
JPEG_FILE: str = get_test_file(JPEG_OBJECT["name"])
MP3_FILE: str = get_test_file(MP3_OBJECT["name"])
MP4_FILE: str = get_test_file(MP4_OBJECT["name"])
PNG_FILE: str = get_test_file(PNG_OBJECT["name"])
ZIP_FILE: str = get_test_file(ZIP_OBJECT["name"])
TTF_FILE: str = get_test_file(TTF_OBJECT["name"])
BAD_FILE: str = get_test_file(BAD_OBJECT["name"])


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
