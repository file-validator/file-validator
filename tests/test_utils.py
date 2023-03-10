"""Tests for utils.py."""
import pytest

from file_validator.constants import ARCHIVE, AUDIO, FILETYPE, FONT, IMAGE, OK, VIDEO
from file_validator.exceptions import (
    EmptyParametersException,
    MimesEqualException,
    TypeNotSupportedException,
)
from file_validator.utils import (
    all_mimes_is_equal,
    generate_information_about_file,
    guess_the_type,
    is_type_supported,
    parameters_are_empty,
)

from tests.fixtures import (
    BAD_FILE,
    MP3_FILE,
    MP3_OBJECT,
    MP4_FILE,
    PNG_FILE,
    PNG_OBJECT,
    TTF_FILE,
    ZIP_FILE,
)


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


class TestAllMimesIsEqual:
    """Tests for all_mimes_is_equal function."""

    @staticmethod
    def test_all_mimes_is_equal_when_use_one_mime():
        """Test all_mimes_is_equal when use one mime."""
        all_mimes_is_equal(["image/png"])

    @staticmethod
    def test_all_mimes_is_equal_when_mimes_is_equal():
        """test all_mimes_is_equal function in utils.py."""
        with pytest.raises(MimesEqualException):
            all_mimes_is_equal([PNG_OBJECT["mime"], PNG_OBJECT["mime"]])

    @staticmethod
    def test_all_mimes_is_equal_when_mimes_is_not_equal():
        """test all_mimes_is_equal function in utils.py."""
        all_mimes_is_equal([PNG_OBJECT["mime"], MP3_OBJECT["mime"]])


class TestIsTypeSupported:
    """Tests for is_type_supported function."""

    @staticmethod
    def test_is_type_supported():
        """Test is_type_supported function when use the not valid type."""
        with pytest.raises(TypeNotSupportedException):
            is_type_supported(acceptable_types=["bad_type"])

    @staticmethod
    def test_is_type_supported_when_use_valid_type():
        """Test is_type_supported function when use the valid type."""
        is_type_supported(acceptable_types=["font"])


class TestParametersAreEmpty:
    """Tests for utils functions."""

    @staticmethod
    def test_parameters_are_empty_when_acceptable_types_and_acceptable_mimes_is_none():
        """Test parameters_are_empty when acceptable_types and acceptable_mimes
        is none."""
        with pytest.raises(EmptyParametersException):
            parameters_are_empty(acceptable_types=None, acceptable_mimes=None)

    @staticmethod
    def test_parameters_are_empty_when_acceptable_types_and_acceptable_mimes_is_not_none():
        """Test parameters_are_empty when acceptable_types and acceptable_mimes
        is not none."""
        parameters_are_empty(
            acceptable_types=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            acceptable_mimes=[PNG_OBJECT["type"], MP3_OBJECT["type"]],
        )


class TestGenerateInformationAboutFile:
    """test for generate_information_about_file function in utils.py."""

    @staticmethod
    def test_generate_information_about_file_when_parameters_is_fill():
        """test generates information about file when parameters are fill."""
        result = generate_information_about_file(
            status=OK,
            library=FILETYPE,
            file_name=PNG_OBJECT["name"],
            file_mime=PNG_OBJECT["mime"],
            file_type=IMAGE,
            file_extension=PNG_OBJECT["extension"],
        )

        assert result["status"] == OK
        assert result["file_type"] == IMAGE
        assert result["library"] == FILETYPE
        assert result["file_name"] == PNG_OBJECT["name"]
        assert result["file_mime"] == PNG_OBJECT["mime"]
        assert result["file_extension"] == PNG_OBJECT["extension"]

    @staticmethod
    def test_generate_information_about_file_when_parameters_is_none():
        """test generates information about file when parameters are none."""
        with pytest.raises(KeyError):
            result = generate_information_about_file()

            assert result["status"] is None
            assert result["file_type"] is None
            assert result["library"] is None
            assert result["file_name"] is None
            assert result["file_mime"] is None
            assert result["file_extension"] is None
