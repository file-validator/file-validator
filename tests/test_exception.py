"""Tests for exception."""
from file_validator.exceptions import error_message

from tests.fixtures import (
    EXPECTED_MESSAGE,
    MIME,
    NAME,
    PNG_OBJECT,
    TEMPLATE_EXPECTED_MESSAGE,
)


class TestException:
    """Tests for exceptions."""

    @staticmethod
    def test_error_message_function_return_correct_message():
        """We test whether this error message function returns the expected
        message or not."""
        message = error_message(
            current_file_name=PNG_OBJECT[NAME],
            current_file_size="20 MB",
            current_file_mime=PNG_OBJECT[MIME],
            acceptable_mimes=["image/png", "audio/mpeg"],
            acceptable_types=["image", "audio"],
            max_file_size="10 MB",
            message=TEMPLATE_EXPECTED_MESSAGE,
        )
        assert EXPECTED_MESSAGE in message
