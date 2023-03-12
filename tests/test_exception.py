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
            message=TEMPLATE_EXPECTED_MESSAGE,
            file_name=PNG_OBJECT[NAME],
            file_size="20 MB",
            mimes=["image/png", "audio/mpeg"],
            max_file_size="10 MB",
            current_file_mime=PNG_OBJECT[MIME],
        )
        assert EXPECTED_MESSAGE in message
