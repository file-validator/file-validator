"""Tests for the command line interface (file_validator.cli)."""
import pytest

from file_validator.cli import main

from tests.fixtures import (
    JPEG_FILE,
    MP3_FILE,
    PNG_FILE,
    PNG_OBJECT,
)


class TestCli:
    """Tests for the file_validator CLI entry point."""

    @staticmethod
    def test_cli_validates_a_valid_file_by_mime():
        """The CLI exits 0 when the file is valid."""
        exit_code = main([PNG_FILE, "--mimes", PNG_OBJECT["mime"]])
        assert exit_code == 0

    @staticmethod
    def test_cli_rejects_an_invalid_file_by_mime():
        """The CLI exits 1 when the file is not valid."""
        exit_code = main([JPEG_FILE, "--mimes", PNG_OBJECT["mime"]])
        assert exit_code == 1

    @staticmethod
    def test_cli_validates_by_extension():
        """The CLI validates files by extension."""
        exit_code = main([PNG_FILE, "--extensions", ".png"])
        assert exit_code == 0

    @staticmethod
    def test_cli_rejects_an_invalid_extension():
        """The CLI exits 1 when the extension is not valid."""
        exit_code = main([PNG_FILE, "--extensions", ".jpg"])
        assert exit_code == 1

    @staticmethod
    def test_cli_validates_by_type():
        """The CLI validates files by type."""
        exit_code = main([PNG_FILE, "--types", "image"])
        assert exit_code == 0

    @staticmethod
    def test_cli_validates_by_size():
        """The CLI validates files by size."""
        exit_code = main([PNG_FILE, "--max-size", "1048576"])
        assert exit_code == 0

    @staticmethod
    def test_cli_rejects_file_over_max_size():
        """The CLI exits 1 when the file is too big."""
        exit_code = main([MP3_FILE, "--max-size", "100"])
        assert exit_code == 1

    @staticmethod
    def test_cli_requires_at_least_one_constraint():
        """The CLI errors out when no constraint is provided."""
        with pytest.raises(SystemExit):
            main([PNG_FILE])
