"""
This module is related to tests
"""
import pytest
import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock
from file_validator.models import ValidatedFileField, FileValidator, FileSizeValidator
from file_validator.utils import all_mimes_is_equal
from tests.fixtures import MP3_OBJECT, JPEG_OBJECT, PNG_OBJECT, JPEG_FILE, MP3_FILE, PNG_FILE, BAD_FILE, TEMPLATE_EXPECTED_MESSAGE, EXPECTED_MESSAGE, TEST_LIBRARY, get_tmp_file, BAD_OBJECT, MAGIC_FILE
from file_validator.validators import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
    size_validator,
    file_validator_by_pure_magic,
    file_validator_by_django
)
from file_validator.constants import PYTHON_MAGIC, FILETYPE, PURE_MAGIC, MIMETYPES, DEFAULT, SELECTING_ALL_SUPPORTED_LIBRARIES, ALL_SUPPORTED_LIBRARIES, FILE_IS_NOT_VALID, DEFAULT_ERROR_MESSAGE, ALL
from file_validator.exceptions import error_message, FileValidationException, SizeValidationException, LibraryNotSupportedException, CUSTOM_ERROR_MESSAGE, MimesEmptyException, DjangoFileValidationException
from tests.project.app.forms import TestFormWithAcceptAttribute, TestFormWithoutAcceptAttribute, TestFormWithCssClassAttribute
from tests.project.app.models import TestFileModel, TestFileModelWithFileValidator, TestFileModelWithFileValidatorSizeIsNone, TestFileModelWithFileValidatorLibraryIsNone, TestFileModelWithFileSizeValidator, TestFileModelWithFileSizeValidatorNotValidSize, TestFileModelWithoutLibraries
from django.core.files.uploadedfile import SimpleUploadedFile


class TestFileValidatorByPythonMagic:
    """
    These tests are for file validators that are made using the python-magic library
    """

    def test_file_validator_by_python_magic_library_when_file_is_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_python_magic(JPEG_OBJECT['mime'], file_path=jpeg) is None

    def test_file_validator_by_python_magic_library_when_file_is_not_valid(self, jpeg=JPEG_FILE):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator_by_python_magic(PNG_OBJECT['mime'], file_path=jpeg)

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_validator_by_python_magic_by_path_magic_file_from_env(self, jpeg=JPEG_FILE):
        assert file_validator_by_python_magic(JPEG_OBJECT['mime'], file_path=jpeg) is None


class TestFileValidatorByMimeTypes:
    """
    These tests are for file validators that are made using the mimetypes library
    """

    def test_file_validator_by_mimetypes_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_mimetypes(JPEG_OBJECT['mime'], file_path=jpeg) is None

    def test_file_validator_by_mimetypes_library_when_file_is_not_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator_by_mimetypes(PNG_OBJECT['mime'], file_path=jpeg)

    def test_mimetypes_library_when_it_could_not_detect_the_mime_file(self):
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_mimetypes(PNG_OBJECT['mime'], file_path=BAD_FILE)


class TestFileValidatorByPureMagic:
    """
    These tests are for file validators that are made using the filetype library
    """

    def test_file_validator_by_pure_magic_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_pure_magic(JPEG_OBJECT['mime'], file_path=jpeg) is None

    def test_file_validator_by_pure_magic_library_when_file_is_not_valid(
        self
    ):
        """
        :param mp3_file: It is a fixture for mp3 files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator_by_pure_magic(JPEG_OBJECT['mime'], file_path=PNG_FILE)

    def test_pure_magic_library_when_it_could_not_detect_the_mime_file(self):
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_pure_magic(PNG_OBJECT['mime'], file_path=BAD_FILE)


class TestFileValidatorByFileType:
    """
    These tests are for file validators that are made using the filetype library
    """

    def test_file_validator_by_filetype_library_when_file_is_valid(
        self, jpeg=JPEG_FILE
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        assert file_validator_by_filetype(JPEG_OBJECT['mime'], file_path=jpeg) is None

    def test_file_validator_by_filetype_library_when_file_is_not_valid(
        self, mp3_file=MP3_FILE
    ):
        """
        :param mp3_file: It is a fixture for mp3 files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator_by_filetype(JPEG_OBJECT['mime'], file_path=mp3_file)

    def test_filetype_library_when_it_could_not_detect_the_mime_file(self):
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_filetype(PNG_OBJECT['mime'], file_path=BAD_FILE)


class TestValidatedFileFieldForm:
    def test_accept_attribute_in_form(self):
        upload_file = open(PNG_FILE, 'rb')
        file_dict = {'test_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = TestFormWithAcceptAttribute({}, file_dict)
        assert form.is_valid()
        assert form.fields['test_file'].accept == 'image/*'

    def test_accept_attribute_is_none_in_form(self):
        form = TestFormWithoutAcceptAttribute()
        assert form.fields['test_file'].accept is None

    def test_css_class_attribute_in_form(self):
        form = TestFormWithCssClassAttribute()
        assert form.fields['test_file'].css_class == 'test-class'


class TestFileValidatorByDjango:
    """
    These tests are for file validators django
    """

    def test_django_file_validator_when_library_is_default_library_and_not_valid_file(self):
        """

        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_django(
                content_type_guessed_by_django=MP3_OBJECT['mime'],
                acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
                libraries=[DEFAULT],
                file_path=MP3_FILE
            )

    def test_when_library_is_not_supported_raise_library_not_supported_exception(self):
        """
        test when the library is not supported raised LibraryNotSupportedException
        """
        with pytest.raises(LibraryNotSupportedException):
            file_validator_by_django(
                content_type_guessed_by_django=MP3_OBJECT['mime'],
                acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
                libraries=[TEST_LIBRARY],
                file_path=MP3_FILE
            )

    def test_django_file_validator_when_library_is_python_magic_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT['mime'],
            acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=[PYTHON_MAGIC],
            file_path=JPEG_FILE
        ) is None

    def test_django_file_validator_when_library_is_pure_magic_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT['mime'],
            acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=[PURE_MAGIC],
            file_path=JPEG_FILE
        ) is None

    def test_django_file_validator_when_library_is_file_type_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT['mime'],
            acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=[FILETYPE],
            file_path=JPEG_FILE
        ) is None

    def test_django_file_validator_when_library_is_mimetypes_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT['mime'],
            acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=[MIMETYPES],
            file_path=JPEG_FILE
        ) is None

    def test_django_file_validator_when_library_is_default_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT['mime'],
            acceptable_mimes=[MP3_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=[DEFAULT],
            file_path=MP3_FILE
        ) is None

    def test_django_file_validator_when_selected_all_library(self):
        """

        :return:
        """
        assert file_validator_by_django(
            content_type_guessed_by_django=JPEG_OBJECT['mime'],
            acceptable_mimes=[PNG_OBJECT['mime'], JPEG_OBJECT['mime']],
            libraries=ALL_SUPPORTED_LIBRARIES,
            file_path=JPEG_FILE
        ) is None


class TestValidatedFileField:
    def test_when_file_is_valid_and_return_none(self):
        new_instance = TestFileModel(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT['name'],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT['mime']
            )
        )

        new_instance.full_clean()

    def test_when_file_is_not_valid_and_raise_validation_error(self):
        new_instance = TestFileModel(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT['name'],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT['mime']
            )
        )

        with pytest.raises(ValidationError):
            new_instance.full_clean()

    def test_deconstruct_method(self):
        my_field_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
            max_upload_file_size=1000000
        )
        name, path, args, kwargs = my_field_instance.deconstruct()
        new_instance = ValidatedFileField(
            libraries=[ALL],
            acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
            max_upload_file_size=1000000
        )
        assert (my_field_instance.libraries, new_instance.libraries)
        assert (my_field_instance.acceptable_mimes, new_instance.acceptable_mimes)
        assert (my_field_instance.max_upload_file_size, new_instance.max_upload_file_size)

    def test_acceptable_mimes_is_none(self):
        with pytest.raises(ValueError):
            class TestFileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                )

    def test_libraries_is_none(self):
        my_field_instance = TestFileModelWithoutLibraries(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT['name'],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT['mime']
            )
        )


class TestFileSizeValidator:
    def test_file_size_is_valid(self):
        new_instance = TestFileModelWithFileSizeValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT['name'],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT['mime']
            )
        )

        new_instance.full_clean()

    def test_file_size_is_not_valid(self):
        with pytest.raises(ValidationError):
            new_instance = TestFileModelWithFileSizeValidatorNotValidSize(
                test_file=get_tmp_file(
                    file_name=PNG_OBJECT['name'],
                    file_path=PNG_FILE,
                    file_mime_type=PNG_OBJECT['mime']
                )
            )

            new_instance.full_clean()

    def test_max_upload_file_size_is_none(self):
        with pytest.raises(SizeValidationException):
            class TestFileModelWithFileValidatorNotMaxUploadSize(models.Model):
                test_file = models.FileField(
                    validators=[
                        FileSizeValidator()
                    ]
                )

    def test_eq_methode(self):
        file_validator_one = FileSizeValidator(
            max_upload_file_size=10485760
        )
        file_validator_two = FileSizeValidator(
            max_upload_file_size=10485760
        )
        assert file_validator_one == file_validator_two


class TestFileValidator:
    def test_when_file_is_valid_and_return_none(self):
        new_instance = TestFileModelWithFileValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT['name'],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT['mime']
            )
        )

        new_instance.full_clean()

    def test_when_file_is_not_valid_and_return_none(self):
        with pytest.raises(ValidationError):
            new_instance = TestFileModelWithFileValidator(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT['name'],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT['mime']
                )
            )

            new_instance.full_clean()

    def test_when_file_size_is_none(self):
        new_instance = TestFileModelWithFileValidatorSizeIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT['name'],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT['mime']
            )
        )

        new_instance.full_clean()

    def test_when_libraries_is_none(self):
        new_instance = TestFileModelWithFileValidatorLibraryIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT['name'],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT['mime']
            )
        )

        new_instance.full_clean()

    def test_when_libraries_is_not_supported(self):
        with pytest.raises(LibraryNotSupportedException):
            class TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                test_file = models.FileField(
                    validators=[
                        FileValidator(
                            acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
                            libraries=[BAD_OBJECT['name']]
                        )
                    ]
                )

    def test_when_acceptable_mimes_is_none(self):
        with pytest.raises(MimesEmptyException):
            class TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                test_file = models.FileField(
                    validators=[
                        FileValidator(
                        )
                    ]
                )

    def test_eq_methode(self):
        file_validator_one = FileValidator(
            acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
            libraries=[ALL]
        )
        file_validator_two = FileValidator(
            acceptable_mimes=[PNG_OBJECT['mime'], MP3_OBJECT['mime']],
            libraries=[ALL]
        )
        assert file_validator_one == file_validator_two


class TestException:
    """
    test
    """

    def test_error_message_function_return_correct_message(self):
        """
        We test whether this error message function returns the expected message or not
        """
        message = error_message(
            message=TEMPLATE_EXPECTED_MESSAGE,
            file=PNG_OBJECT['name'],
            file_size="20 MB",
            mimes=["image/png", "audio/mpeg"],
            max_file_size="10 MB",
        )
        assert EXPECTED_MESSAGE in message


def test_file_validator_when_file_is_valid(jpeg=JPEG_FILE):
    """
    :param jpeg: It is a fixture for jpeg files
    :return: The result we expect to return is None, which means that everything is OK
    """
    assert file_validator(JPEG_OBJECT['mime'], file_path=jpeg) is None


def test_size_validator():
    """
    :return:
    """
    with pytest.raises(SizeValidationException):
        assert size_validator(
            max_upload_file_size=1,
            file_path=PNG_FILE
        )


def test_all_mimes_is_equal():
    assert all_mimes_is_equal(["image/png"]) is False
