"""Tests for ValidatedFileField."""
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from file_validator.constants import ALL
from file_validator.exceptions import (
    EmptyParametersException,
    MimesEqualException,
    TypeNotSupportedException,
)
from file_validator.models import ValidatedFileField

from tests.fixtures import (
    BAD_OBJECT,
    get_tmp_file,
    JPEG_FILE,
    JPEG_OBJECT,
    MP3_OBJECT,
    PNG_FILE,
    PNG_OBJECT,
)
from tests.project.app.forms import (
    TestForm,
    TestFormWithCssClassAttribute,
    TestFormWithoutAcceptAttribute,
)
from tests.project.app.models import (
    TestModelWithValidatedFileField,
    TestModelWithValidatedFileFieldAndAllLibrary,
    TestModelWithValidatedFileFieldAndDjangoLibrary,
    TestModelWithValidatedFileFieldAndFileTypeLibrary,
    TestModelWithValidatedFileFieldAndMimetypesLibrary,
    TestModelWithValidatedFileFieldAndPureMagicLibrary,
    TestModelWithValidatedFileFieldAndPythonMagicLibrary,
    TestModelWithValidatedFileFieldWithAcceptableType,
    TestModelWithValidatedFileFieldWithoutLibrary,
)


class TestValidatedFileFieldModel:
    """tests for ValidatedFileField."""

    @staticmethod
    def test_validated_file_field_with_all_libraries():
        """Test ValidatedFileField with all libraries."""
        _my_field_instance = TestModelWithValidatedFileFieldAndAllLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_file_is_valid_and_return_none():
        """test ValidatedFileField when file is valid and return none."""
        new_instance = TestModelWithValidatedFileField(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_file_is_not_valid_and_raise_validation_error():
        """test ValidatedFileField when file is not valid and raise validation
        error."""
        new_instance = TestModelWithValidatedFileField(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT["name"],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT["mime"],
            ),
        )

        with pytest.raises(ValidationError):
            new_instance.full_clean()

    @staticmethod
    def test_validated_file_field_deconstruct_method():
        """test deconstruct method."""
        my_field_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            max_upload_file_size=1000000,
        )
        _name, _path, _args, _kwargs = my_field_instance.deconstruct()
        new_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            max_upload_file_size=1000000,
        )
        assert my_field_instance.libraries, new_instance.libraries
        assert my_field_instance.acceptable_mimes, new_instance.acceptable_mimes
        assert my_field_instance.max_upload_file_size, new_instance.max_upload_file_size

    @staticmethod
    def test_validated_file_field_acceptable_mimes_is_none():
        """test acceptable mimes in ValidatedFileField is none."""
        with pytest.raises(EmptyParametersException):

            class _TestFileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                )

    @staticmethod
    def test_validated_file_field_libraries_is_none():
        """the test ValidatedFileField library is none."""
        _my_field_instance = TestModelWithValidatedFileFieldWithoutLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_acceptable_types_when_type_not_supported():
        """Test acceptable types in ValidatedFileField when the type not
        supported."""
        with pytest.raises(TypeNotSupportedException):

            class _FileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                    acceptable_types=[BAD_OBJECT["type"]],
                )

    @staticmethod
    def test_validated_file_field_acceptable_mimes_is_not_none_and_all_mimes_is_equal():
        """Test acceptable types in ValidatedFileField when the type not
        supported."""
        with pytest.raises(MimesEqualException):

            class _FileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                    acceptable_mimes=[BAD_OBJECT["mime"], BAD_OBJECT["mime"]],
                )

    @staticmethod
    def test_validated_file_field_when_acceptable_types_is_fill():
        """Test ValidatedFileField when acceptable_types is fill."""
        _my_field_instance = TestModelWithValidatedFileFieldWithAcceptableType(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_python_magic():
        """Test ValidatedFileField when the library is python magic and the
        file is valid."""
        _my_field_instance = TestModelWithValidatedFileFieldAndPythonMagicLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_pure_magic():
        """Test ValidatedFileField when the library is puremagic and file is
        valid."""
        _my_field_instance = TestModelWithValidatedFileFieldAndPureMagicLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_mimetypes():
        """Test ValidatedFileField when the library is mimetypes and file is
        valid."""
        _my_field_instance = TestModelWithValidatedFileFieldAndMimetypesLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_filetype():
        """Test ValidatedFileField when the library is filetype and file is
        valid."""
        _my_field_instance = TestModelWithValidatedFileFieldAndFileTypeLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_django():
        """Test ValidatedFileField when the library is django and file is
        valid."""
        _my_field_instance = TestModelWithValidatedFileFieldAndDjangoLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_django_and_file_is_not_valid():
        """Test ValidatedFileField when the library is django and file is not
        valid."""
        with pytest.raises(ValidationError):
            _my_field_instance = TestModelWithValidatedFileFieldAndDjangoLibrary(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT["name"],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT["mime"],
                ),
            )
            _my_field_instance.full_clean()


class TestValidatedFileFieldForm:
    """test for ValidatedFileField Forms."""

    @staticmethod
    def test_accept_attribute_in_form():
        """test accept attribute in form."""
        with open(PNG_FILE, "rb") as file:
            upload_file = file
            file_dict = {
                "test_file": SimpleUploadedFile(upload_file.name, upload_file.read()),
            }
            form = TestForm({}, file_dict)
            assert form.is_valid()
            assert form.fields["test_file"].accept == "image/*"
            assert form.fields["test_file"].multiple is True

    @staticmethod
    def test_accept_attribute_is_none_in_form():
        """test accept attribute is none in form."""
        form = TestFormWithoutAcceptAttribute()
        assert form.fields["test_file"].accept is None

    @staticmethod
    def test_css_class_attribute_in_form():
        """test css class attribute in form."""
        form = TestFormWithCssClassAttribute()
        assert form.fields["test_file"].custom_css_class == "test-class"
