"""Tests for guess_the_type function in utils.py."""
from file_validator.constants import ARCHIVE, AUDIO, FONT, IMAGE, VIDEO
from file_validator.utils import guess_the_type

from tests.fixtures import BAD_FILE, MP3_FILE, MP4_FILE, PNG_FILE, TTF_FILE, ZIP_FILE


class TestGuessTheType:
    """test for guess_the_type function in utils.py."""

    @staticmethod
    def test_guess_the_type_function_when_file_is_invalid_and_return_none():
        """test guesses the type function when file is invalid and return
        none."""
        file_type = guess_the_type(file_path=BAD_FILE)
        assert file_type is None

    @staticmethod
    def test_guess_the_type_function_when_file_is_archive():
        """test guesses the type function when file is archive."""
        file_type = guess_the_type(file_path=ZIP_FILE)
        assert file_type is ARCHIVE

    @staticmethod
    def test_guess_the_type_function_when_file_is_image():
        """test guesses the type function when file is image."""
        file_type = guess_the_type(file_path=PNG_FILE)
        assert file_type is IMAGE

    @staticmethod
    def test_guess_the_type_function_when_file_is_video():
        """test guesses the type function when file is video."""
        file_type = guess_the_type(file_path=MP4_FILE)
        assert file_type is VIDEO

    @staticmethod
    def test_guess_the_type_function_when_file_is_audio():
        """test guesses the type function when file is audio."""
        file_type = guess_the_type(file_path=MP3_FILE)
        assert file_type is AUDIO

    @staticmethod
    def test_guess_the_type_function_when_file_is_font():
        """test guesses the type function when file is font."""
        file_type = guess_the_type(file_path=TTF_FILE)
        assert file_type is FONT
