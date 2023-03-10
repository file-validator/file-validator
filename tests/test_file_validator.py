"""This module is related to tests."""
import os
from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from file_validator.constants import (
    ALL,
    ALL_SUPPORTED_LIBRARIES,
    ARCHIVE,
    AUDIO,
    DEFAULT,
    FILETYPE,
    FONT,
    IMAGE,
    MIMETYPES,
    OK,
    PURE_MAGIC,
    PYTHON_MAGIC,
    VIDEO,
)
from file_validator.exceptions import (
    EmptyParametersException,
    error_message,
    FileValidationException,
    LibraryNotSupportedException,
    MimesEmptyException,
    MimesEqualException,
    SizeValidationException,
    TypeNotSupportedException,
)
from file_validator.models import (
    DjangoFileValidator,
    FileSizeValidator,
    ValidatedFileField,
)
from file_validator.utils import (
    all_mimes_is_equal,
    generate_information_about_file,
    guess_the_type,
    is_type_supported,
    parameters_are_empty,
)
from file_validator.validators import FileValidator

from tests.fixtures import (
    BAD_FILE,
    BAD_OBJECT,
    EXPECTED_MESSAGE,
    get_tmp_file,
    JPEG_FILE,
    JPEG_OBJECT,
    MAGIC_FILE,
    MP3_FILE,
    MP3_OBJECT,
    MP4_FILE,
    PNG_FILE,
    PNG_OBJECT,
    TEMPLATE_EXPECTED_MESSAGE,
    TEST_LIBRARY,
    TTF_FILE,
    ZIP_FILE,
)
from tests.project.app.forms import (
    TestForm,
    TestFormWithCssClassAttribute,
    TestFormWithoutAcceptAttribute,
)
from tests.project.app.models import (
    TestModelWithDjangoFileValidator,
    TestModelWithDjangoFileValidatorAndLibraryIsDjango,
    TestModelWithDjangoFileValidatorAndLibraryIsFiletype,
    TestModelWithDjangoFileValidatorAndLibraryIsMimetypes,
    TestModelWithDjangoFileValidatorAndLibraryIsNone,
    TestModelWithDjangoFileValidatorAndLibraryIsPureMagic,
    TestModelWithDjangoFileValidatorAndLibraryIsPythonMagic,
    TestModelWithDjangoFileValidatorAndSizeIsNone,
    TestModelWithDjangoFileValidatorWithAcceptableType,
    TestModelWithFileSizeValidator,
    TestModelWithFileSizeValidatorAndNotValidSize,
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


class TestFileValidatorByPythonMagic:
    """These tests are for file validators that are made using the python-magic
    library."""

    @staticmethod
    def test_file_validator_by_python_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT["mime"]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.python_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_file_validator_by_python_magic_library_when_file_is_not_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"]],
                file_path=jpeg,
            )
            file_validator.python_magic()

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_validator_by_python_magic_by_path_magic_file_from_env(
        self,
        jpeg=JPEG_FILE,
    ):
        """test file_validator_by_python_magic by path_magic file from .env
        file."""
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT["mime"]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.python_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]


class TestFileValidatorByMimeTypes:
    """These tests are for file validators that are made using the mimetypes
    library."""

    @staticmethod
    def test_file_validator_by_mimetypes_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT["mime"]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.mimetypes()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_file_validator_by_mimetypes_library_when_file_is_not_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"]],
                file_path=jpeg,
            )
            file_validator.mimetypes()

    @staticmethod
    def test_mimetypes_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"]],
                file_path=BAD_FILE,
            )
            file_validator.mimetypes()


class TestFileValidatorByPureMagic:
    """These tests are for file validators that are made using the filetype
    library."""

    @staticmethod
    def test_file_validator_by_pure_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT["mime"]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.pure_magic()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_file_validator_by_pure_magic_library_when_file_is_not_valid():
        """
        :param mp3_file: It is a fixture for mp3 files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[JPEG_OBJECT["mime"]],
                file_path=PNG_FILE,
            )
            file_validator.pure_magic()

    @staticmethod
    def test_pure_magic_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"]],
                file_path=BAD_FILE,
            )
            file_validator.pure_magic()


class TestFileValidatorByFileType:
    """These tests are for file validators that are made using the filetype
    library."""

    @staticmethod
    def test_file_validator_by_filetype_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        file_validator = FileValidator(
            acceptable_mimes=[JPEG_OBJECT["mime"]],
            file_path=jpeg,
        )
        result_of_validation = file_validator.filetype()
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_file_validator_by_filetype_library_when_file_is_not_valid(
        mp3_file=MP3_FILE,
    ):
        """
        :param mp3_file: It is a fixture for mp3 files
        :return: The result we expect is a return value error, which means that the file is invalid
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[JPEG_OBJECT["mime"]],
                file_path=mp3_file,
            )
            file_validator.filetype()

    @staticmethod
    def test_filetype_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_mimes=[PNG_OBJECT["mime"]],
                file_path=BAD_FILE,
            )
            file_validator.filetype()


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


class TestFileExtensionValidator:
    """Test validate_extension method."""

    @staticmethod
    def test_file_extension_validator_when_file_is_valid():
        """Test file extension validator when file is valid."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_extensions=[PNG_OBJECT["extension"]],
        )
        file_validator.validate_extension()

    @staticmethod
    def test_file_extension_validator_when_file_is_not_valid():
        """Test file extension validator when file is not valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_path=PNG_FILE,
                acceptable_extensions=[JPEG_OBJECT["extension"]],
            )
            file_validator.validate_extension()


class TestFileValidatorByType:
    """tests for file_validator_by_type function."""

    @staticmethod
    def test_file_validator_by_type_when_type_is_not_supported():
        """test for file_validator_by_type when type is not supported."""
        with pytest.raises(TypeNotSupportedException):
            file_validator = FileValidator(
                acceptable_types=["test_type"],
                file_path=PNG_FILE,
            )
            file_validator.validate_type()

    @staticmethod
    def test_file_validator_by_type_when_return_file_validation_exception():
        """test for file_validator_by_type when return file validation
        exception."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                acceptable_types=[VIDEO, AUDIO],
                file_path=PNG_FILE,
            )
            file_validator.validate_type()

    @staticmethod
    def test_file_validator_by_type_when_return_validation_data_and_file_is_valid():
        """test for file_validator_by_type when return validation data and file
        is valid."""
        file_validator = FileValidator(
            acceptable_types=[IMAGE, AUDIO],
            file_path=PNG_FILE,
        )
        result_of_validation = file_validator.validate_type()
        assert result_of_validation["status"] == OK
        assert result_of_validation["library"] == FILETYPE
        assert result_of_validation["file_name"] == PNG_OBJECT["name"]


class TestDjangoFileValidator:
    """test for file validator."""

    @staticmethod
    def test_django_file_validator_when_file_is_valid_and_return_none():
        """test when file is valid and return none."""
        new_instance = TestModelWithDjangoFileValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_file_is_not_valid_and_return_none():
        """test when file is not valid and return none."""
        with pytest.raises(ValidationError):
            new_instance = TestModelWithDjangoFileValidator(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT["name"],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT["mime"],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_file_size_is_none():
        """test when file size is none."""
        new_instance = TestModelWithDjangoFileValidatorAndSizeIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_libraries_is_none():
        """test when libraries is none."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_libraries_is_not_supported():
        """test when libraries is not supported."""
        with pytest.raises(LibraryNotSupportedException):

            class _TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                """Test Model."""

                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                            libraries=[BAD_OBJECT["name"]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_acceptable_mimes_is_not_none_and_all_mimes_is_equal():
        """test when acceptable mimes is none."""
        with pytest.raises(MimesEqualException):

            class _TestFileModelWithDjangoFileValidatorAndNoneParameters(models.Model):
                """Test Model."""

                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            acceptable_mimes=[PNG_OBJECT["mime"], PNG_OBJECT["mime"]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_eq_methode():
        """test eq methode."""
        file_validator_one = DjangoFileValidator(
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            libraries=[ALL],
        )
        file_validator_two = DjangoFileValidator(
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
            libraries=[ALL],
        )
        assert file_validator_one == file_validator_two

    @staticmethod
    def test_django_file_validator_hash_method():
        """Test for __hash__ method in FileValidator."""
        test_file = DjangoFileValidator(
            max_upload_file_size=1000,
            acceptable_mimes=[PNG_OBJECT["mime"]],
        )
        assert hash(test_file) == 1000

    @staticmethod
    def test_django_file_validator_acceptable_types_when_type_not_supported():
        """Test acceptable types in ValidatedFileField when the type not
        supported."""
        with pytest.raises(TypeNotSupportedException):

            class TestModelWithDjangoFileValidatorAndBadAcceptableType(models.Model):
                test_file = models.FileField(
                    validators=[
                        DjangoFileValidator(
                            libraries=[ALL],
                            max_upload_file_size=1000000,
                            acceptable_types=[BAD_OBJECT["type"]],
                        ),
                    ],
                )

    @staticmethod
    def test_django_file_validator_when_library_is_python_magic():
        """Test django file validator when the library is python magic."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsPythonMagic(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_pure_magic():
        """Test django file validator when the library is pure magic."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsPureMagic(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_mimetypes():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsMimetypes(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_filetype():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsFiletype(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_library_is_django():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorAndLibraryIsDjango(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_django_file_validator_when_acceptable_types_is_fill():
        """Test django file validator when the library is mimetypes."""
        new_instance = TestModelWithDjangoFileValidatorWithAcceptableType(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()


class TestFileValidatorDjango:
    """Test."""

    @staticmethod
    def test_file_validation_by_django_data_when_file_is_not_valid():
        """Test."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_mime_guessed_by_django=JPEG_OBJECT["mime"],
                acceptable_mimes=[PNG_OBJECT["mime"]],
            )
            file_validator.django()

    @staticmethod
    def test_validate_method_when_file_mime_guessed_parameter_by_django_is_not_fill():
        """Test."""
        file_validator = FileValidator(
            acceptable_mimes=[PNG_OBJECT["mime"]],
            file_path=PNG_FILE,
        )
        file_validator.validate()


class TestValidatedFileField:
    """tests for ValidatedFileField."""

    @staticmethod
    def test_validated_file_field_with_all_libraries():
        """Test."""
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
        """Test."""
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
        """Test."""
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
        """Test."""
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
        """Test."""
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
        """Test."""
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
        """Test."""
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
        """Test."""
        with pytest.raises(ValidationError):
            _my_field_instance = TestModelWithValidatedFileFieldAndDjangoLibrary(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT["name"],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT["mime"],
                ),
            )
            _my_field_instance.full_clean()


class TestFileSizeValidator:
    """test file size validator."""

    @staticmethod
    def test_file_size_is_valid():
        """test file size is valid."""
        new_instance = TestModelWithFileSizeValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_file_size_is_not_valid():
        """test file size is not valid."""
        with pytest.raises(ValidationError):
            new_instance = TestModelWithFileSizeValidatorAndNotValidSize(
                test_file=get_tmp_file(
                    file_name=PNG_OBJECT["name"],
                    file_path=PNG_FILE,
                    file_mime_type=PNG_OBJECT["mime"],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_max_upload_file_size_is_none():
        """test max upload file size is none."""
        with pytest.raises(SizeValidationException):

            class _TestFileModelWithFileValidatorNotMaxUploadSize(models.Model):
                test_file = models.FileField(validators=[FileSizeValidator()])

    @staticmethod
    def test_eq_method():
        """test eq method."""
        file_validator_one = FileSizeValidator(max_upload_file_size=10485760)
        file_validator_two = FileSizeValidator(max_upload_file_size=10485760)
        assert file_validator_one == file_validator_two

    @staticmethod
    def test_hash_method():
        """Test for __hash__ method in FileSizeValidator."""
        test_file = FileSizeValidator(
            max_upload_file_size=1000,
        )
        assert hash(test_file) == 1000


class TestFileMimeValidator:
    """Test validate_mime method."""

    @staticmethod
    def test_file_mime_validation_when_mime_file_is_valid():
        """Test file mime validation when mime file is valid."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_mimes=[PNG_OBJECT["mime"]],
        )
        file_validator.validate_mime()

    @staticmethod
    def test_file_mime_validation_when_mime_file_is_not_valid():
        """Test file mime validation when mime file is not valid."""
        with pytest.raises(FileValidationException):
            file_validator = FileValidator(
                file_path=PNG_FILE,
                acceptable_mimes=[JPEG_OBJECT["mime"]],
            )
            file_validator.validate_mime()

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_mime_validation_by_path_magic_file_from_env(
        self,
    ):
        """Test file mime validation by path magic file from env file."""
        file_validator = FileValidator(
            file_path=PNG_FILE,
            acceptable_mimes=[PNG_OBJECT["mime"]],
        )
        file_validator.validate_mime()


class TestFileValidator:
    """Test."""

    @staticmethod
    def test_size_validator():
        """
        :return:
        """
        with pytest.raises(SizeValidationException):
            file_validator = FileValidator(max_upload_file_size=1, file_path=PNG_FILE)
            file_validator.validate_size()


class TestGuessTheType:
    """test for guess_the_type function in utils.py."""

    @staticmethod
    def test_guess_the_type_function_when_file_is_invalid_and_return_none():
        """test guess the type function when file is invalid and return
        none."""
        file_type = guess_the_type(file_path=BAD_FILE)
        assert file_type is None

    @staticmethod
    def test_guess_the_type_function_when_file_is_archive():
        """test guess the type function when file is archive."""
        file_type = guess_the_type(file_path=ZIP_FILE)
        assert file_type is ARCHIVE

    @staticmethod
    def test_guess_the_type_function_when_file_is_image():
        """test guess the type function when file is image."""
        file_type = guess_the_type(file_path=PNG_FILE)
        assert file_type is IMAGE

    @staticmethod
    def test_guess_the_type_function_when_file_is_video():
        """test guess the type function when file is video."""
        file_type = guess_the_type(file_path=MP4_FILE)
        assert file_type is VIDEO

    @staticmethod
    def test_guess_the_type_function_when_file_is_audio():
        """test guesses the type function when file is audio."""
        file_type = guess_the_type(file_path=MP3_FILE)
        assert file_type is AUDIO

    @staticmethod
    def test_guess_the_type_function_when_file_is_font():
        """test guess the type function when file is font."""
        file_type = guess_the_type(file_path=TTF_FILE)
        assert file_type is FONT


class TestException:
    """test."""

    @staticmethod
    def test_error_message_function_return_correct_message():
        """We test whether this error message function returns the expected
        message or not."""
        message = error_message(
            message=TEMPLATE_EXPECTED_MESSAGE,
            file_name=PNG_OBJECT["name"],
            file_size="20 MB",
            mimes=["image/png", "audio/mpeg"],
            max_file_size="10 MB",
            current_file_mime=PNG_OBJECT["mime"],
        )
        assert EXPECTED_MESSAGE in message


class TestUtils:
    """Tests for utils functions."""

    @staticmethod
    def test_all_mimes_is_equal():
        """test all_mimes_is_equal function in utils.py."""
        all_mimes_is_equal(["image/png"])

    @staticmethod
    def test_parameters_are_empty():
        with pytest.raises(EmptyParametersException):
            parameters_are_empty(acceptable_types=None, acceptable_mimes=None)

    @staticmethod
    def test_is_type_supported():
        with pytest.raises(TypeNotSupportedException):
            is_type_supported(acceptable_types=["bad_type"])

    @staticmethod
    def test_is_type_supported__when_use_valid_type():
        is_type_supported(acceptable_types=["font"])
