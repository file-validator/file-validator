"""Tests for utils.py."""
import pytest

from file_validator.exceptions import (
    EmptyParametersException,
    TypeNotSupportedException,
)
from file_validator.utils import (
    all_mimes_is_equal,
    is_type_supported,
    parameters_are_empty,
)


class TestUtils:
    """Tests for utils functions."""

    @staticmethod
    def test_all_mimes_is_equal():
        """test all_mimes_is_equal function in utils.py."""
        all_mimes_is_equal(["image/png"])

    @staticmethod
    def test_parameters_are_empty():
        """Test parameters_are_empty function."""
        with pytest.raises(EmptyParametersException):
            parameters_are_empty(acceptable_types=None, acceptable_mimes=None)

    @staticmethod
    def test_is_type_supported():
        """Test is_type_supported function when use the not valid type."""
        with pytest.raises(TypeNotSupportedException):
            is_type_supported(acceptable_types=["bad_type"])

    @staticmethod
    def test_is_type_supported_when_use_valid_type():
        """Test is_type_supported function when use the valid type."""
        is_type_supported(acceptable_types=["font"])
