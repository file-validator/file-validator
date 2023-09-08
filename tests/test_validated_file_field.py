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
    MIME,
    MP3_OBJECT,
    NAME,
    PNG_FILE,
    PNG_OBJECT,
    TYPE,
)
from tests.project.app.forms import (
    FormWithCssClassAttribute,
    FormWithoutAcceptAttribute,
    FormWithValidatedFileField,
)
from tests.project.app.models import (
    ModelWithValidatedFileField,
    ModelWithValidatedFileFieldAndAllLibrary,
    ModelWithValidatedFileFieldAndDjangoLibrary,
    ModelWithValidatedFileFieldAndFileTypeLibrary,
    ModelWithValidatedFileFieldAndMimetypesLibrary,
    ModelWithValidatedFileFieldAndPureMagicLibrary,
    ModelWithValidatedFileFieldAndPythonMagicLibrary,
    ModelWithValidatedFileFieldWithAcceptableType,
    ModelWithValidatedFileFieldWithoutLibrary,
)


class TestValidatedFileFieldModel:
    """Tests for ValidatedFileField."""

    @staticmethod
    def test_validated_file_field_with_all_libraries():
        """Test ValidatedFileField with all libraries."""
        _my_field_instance = ModelWithValidatedFileFieldAndAllLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_file_is_valid_and_return_none():
        """Test ValidatedFileField when file is valid and return none."""
        new_instance = ModelWithValidatedFileField(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_file_is_not_valid_and_raise_validation_error():
        """Test ValidatedFileField when file is not valid and raise validation
        error."""
        new_instance = ModelWithValidatedFileField(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT[NAME],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT[MIME],
            ),
        )

        with pytest.raises(ValidationError):
            new_instance.full_clean()

    @staticmethod
    def test_validated_file_field_deconstruct_method():
        """Test deconstruct method."""
        my_field_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT[MIME], MP3_OBJECT[MIME]],
            max_upload_file_size=1000000,
        )
        _name, _path, _args, _kwargs = my_field_instance.deconstruct()
        new_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT[MIME], MP3_OBJECT[MIME]],
            max_upload_file_size=1000000,
        )
        assert my_field_instance.libraries, new_instance.libraries
        assert my_field_instance.acceptable_mimes, new_instance.acceptable_mimes
        assert my_field_instance.max_upload_file_size, new_instance.max_upload_file_size

    @staticmethod
    def test_validated_file_field_acceptable_mimes_is_none():
        """Test acceptable mimes in ValidatedFileField is none."""
        with pytest.raises(EmptyParametersException):
            class _TestFileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                )

    @staticmethod
    def test_validated_file_field_libraries_is_none():
        """The test ValidatedFileField library is none."""
        _my_field_instance = ModelWithValidatedFileFieldWithoutLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
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
                    acceptable_types=[BAD_OBJECT[TYPE]],
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
                    acceptable_mimes=[BAD_OBJECT[MIME], BAD_OBJECT[MIME]],
                )

    @staticmethod
    def test_validated_file_field_when_acceptable_types_is_fill():
        """Test ValidatedFileField when acceptable_types is fill."""
        _my_field_instance = ModelWithValidatedFileFieldWithAcceptableType(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_python_magic():
        """Test ValidatedFileField when the library is python magic and the
        file is valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndPythonMagicLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_pure_magic():
        """Test ValidatedFileField when the library is puremagic and file is
        valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndPureMagicLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_mimetypes():
        """Test ValidatedFileField when the library is mimetypes and file is
        valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndMimetypesLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_filetype():
        """Test ValidatedFileField when the library is filetype and file is
        valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndFileTypeLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_django():
        """Test ValidatedFileField when the library is django and file is
        valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndDjangoLibrary(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT[NAME],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT[MIME],
            ),
        )
        _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_library_is_django_and_file_is_not_valid():
        """Test ValidatedFileField when the library is django and file is not
        valid."""
        with pytest.raises(ValidationError):
            _my_field_instance = ModelWithValidatedFileFieldAndDjangoLibrary(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT[NAME],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT[MIME],
                ),
            )
            _my_field_instance.full_clean()

    @staticmethod
    def test_validated_file_field_when_file_mime_guessed_by_django_is_none():
        """Test ValidatedFileField when the library is django and file is not
        valid."""
        _my_field_instance = ModelWithValidatedFileFieldAndDjangoLibrary(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT[NAME],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT[MIME],
            ),
        )
        del _my_field_instance.test_file.file.content_type
        _my_field_instance.full_clean()


class TestValidatedFileFieldForm:
    """Test for ValidatedFileField Forms."""

    @staticmethod
    def test_accept_attribute_in_form():
        """Test accept attribute in form."""
        with open(PNG_FILE, "rb") as file:
            upload_file = file
            file_dict = {
                "test_file": SimpleUploadedFile(upload_file.name, upload_file.read()),
            }
            form = FormWithValidatedFileField({}, file_dict)
            assert form.is_valid()
            assert form.fields["test_file"].accept == "image/*"
            assert form.fields["test_file"].multiple is True

    @staticmethod
    def test_accept_attribute_is_none_in_form():
        """Test accept attribute is none in form."""
        form = FormWithoutAcceptAttribute()
        assert form.fields["test_file"].accept is None

    @staticmethod
    def test_css_class_attribute_in_form():
        """Test css class attribute in form."""
        form = FormWithCssClassAttribute()
        assert form.fields["test_file"].custom_css_class == "test-class"
