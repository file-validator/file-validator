"""
This module is related to tests
"""
import os
from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from file_validator.constants import (
    PYTHON_MAGIC,
    FILETYPE,
    PURE_MAGIC,
    MIMETYPES,
    DEFAULT,
    ALL_SUPPORTED_LIBRARIES,
    ALL,
    OK,
    IMAGE,
    VIDEO,
    AUDIO,
    ARCHIVE,
    FONT,
)
from file_validator.exceptions import (
    error_message,
    FileValidationException,
    SizeValidationException,
    LibraryNotSupportedException,
    MimesEmptyException,
    TypeNotSupportedException,
)
from file_validator.models import ValidatedFileField, FileValidator, FileSizeValidator
from file_validator.utils import (
    all_mimes_is_equal,
    generate_information_about_file,
    guess_the_type,
)
from file_validator.validators import (
    file_validator_by_python_magic,
    file_validator_by_mimetypes,
    file_validator_by_filetype,
    file_validator,
    size_validator,
    file_validator_by_pure_magic,
    file_validator_by_django,
    file_validator_by_type,
)
from tests.fixtures import (
    MP3_OBJECT,
    JPEG_OBJECT,
    PNG_OBJECT,
    JPEG_FILE,
    MP3_FILE,
    PNG_FILE,
    BAD_FILE,
    TEMPLATE_EXPECTED_MESSAGE,
    EXPECTED_MESSAGE,
    TEST_LIBRARY,
    get_tmp_file,
    BAD_OBJECT,
    MAGIC_FILE,
    MP4_FILE,
    ZIP_FILE,
    TTF_FILE,
)
from tests.project.app.forms import (
    TestFormWithoutAcceptAttribute,
    TestFormWithCssClassAttribute,
    TestForm,
)
from tests.project.app.models import (
    TestFileModel,
    TestFileModelWithFileValidator,
    TestFileModelWithFileValidatorSizeIsNone,
    TestFileModelWithFileValidatorLibraryIsNone,
    TestFileModelWithFileSizeValidator,
    TestFileModelWithFileSizeValidatorNotValidSize,
    TestFileModelWithoutLibraries,
)


class TestGenerateInformationAboutFile:
    """
    test for generate_information_about_file function in utils.py
    """

    @staticmethod
    def test_generate_information_about_file_when_parameters_is_fill():
        """
        test generates information about file when parameters are fill
        """
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
        """
        test generates information about file when parameters are none
        """
        with pytest.raises(KeyError):

            result = generate_information_about_file()

            assert result["status"] is None
            assert result["file_type"] is None
            assert result["library"] is None
            assert result["file_name"] is None
            assert result["file_mime"] is None
            assert result["file_extension"] is None


class TestFileValidatorByPythonMagic:
    """
    These tests are for file validators that are made using the python-magic library
    """

    @staticmethod
    def test_file_validator_by_python_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        result_of_validation = file_validator_by_python_magic(
            JPEG_OBJECT["mime"], file_path=jpeg,
        )
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
            file_validator_by_python_magic(PNG_OBJECT["mime"], file_path=jpeg)

    @mock.patch.dict(os.environ, {"path_magic_file": MAGIC_FILE}, clear=True)
    def test_file_validator_by_python_magic_by_path_magic_file_from_env(
        self, jpeg=JPEG_FILE,
    ):
        """
        test file_validator_by_python_magic by path_magic file from .env file
        """
        result_of_validation = file_validator_by_python_magic(
            JPEG_OBJECT["mime"], file_path=jpeg,
        )
        assert result_of_validation["status"] == OK
        assert result_of_validation["file_name"] == JPEG_OBJECT["name"]
        assert result_of_validation["file_mime"] == JPEG_OBJECT["mime"]
        assert result_of_validation["file_type"] == JPEG_OBJECT["type"]
        assert result_of_validation["file_extension"] == JPEG_OBJECT["extension"]


class TestFileValidatorByMimeTypes:
    """
    These tests are for file validators that are made using the mimetypes library
    """

    @staticmethod
    def test_file_validator_by_mimetypes_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        result_of_validation = file_validator_by_mimetypes(
            JPEG_OBJECT["mime"], file_path=jpeg,
        )
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
            file_validator_by_mimetypes(PNG_OBJECT["mime"], file_path=jpeg)

    @staticmethod
    def test_mimetypes_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_mimetypes(PNG_OBJECT["mime"], file_path=BAD_FILE)


class TestFileValidatorByPureMagic:
    """
    These tests are for file validators that are made using the filetype library
    """

    @staticmethod
    def test_file_validator_by_pure_magic_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        result_of_validation = file_validator_by_pure_magic(
            JPEG_OBJECT["mime"], file_path=jpeg,
        )
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
            file_validator_by_pure_magic(JPEG_OBJECT["mime"], file_path=PNG_FILE)

    @staticmethod
    def test_pure_magic_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_pure_magic(PNG_OBJECT["mime"], file_path=BAD_FILE)


class TestFileValidatorByFileType:
    """
    These tests are for file validators that are made using the filetype library
    """

    @staticmethod
    def test_file_validator_by_filetype_library_when_file_is_valid(
        jpeg=JPEG_FILE,
    ):
        """
        :param jpeg: It is a fixture for jpeg files
        :return: The result we expect to return is None, which means that everything is OK
        """
        result_of_validation = file_validator_by_filetype(
            JPEG_OBJECT["mime"], file_path=jpeg,
        )
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
            file_validator_by_filetype(JPEG_OBJECT["mime"], file_path=mp3_file)

    @staticmethod
    def test_filetype_library_when_it_could_not_detect_the_mime_file():
        """
        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_filetype(PNG_OBJECT["mime"], file_path=BAD_FILE)


class TestValidatedFileFieldForm:
    """
    test for ValidatedFileField Forms
    """

    @staticmethod
    def test_accept_attribute_in_form():
        """
        test accept attribute in form
        """
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
        """
        test accept attribute is none in form
        """
        form = TestFormWithoutAcceptAttribute()
        assert form.fields["test_file"].accept is None

    @staticmethod
    def test_css_class_attribute_in_form():
        """
        test css class attribute in form
        """
        form = TestFormWithCssClassAttribute()
        assert form.fields["test_file"].custom_css_class == "test-class"


class TestFileValidatorByDjango:
    """
    These tests are for file validators django
    """

    @staticmethod
    def test_file_validator_by_django_when_library_is_default_library_and_not_valid_file():
        """

        :return:
        """
        with pytest.raises(FileValidationException):
            file_validator_by_django(
                content_type_guessed_by_django=MP3_OBJECT["mime"],
                acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
                libraries=[DEFAULT],
                file_path=MP3_FILE,
            )

    @staticmethod
    def test_when_library_is_not_supported_raise_library_not_supported_exception():
        """
        test when the library is not supported raised LibraryNotSupportedException
        """
        with pytest.raises(LibraryNotSupportedException):
            file_validator_by_django(
                content_type_guessed_by_django=MP3_OBJECT["mime"],
                acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                libraries=[TEST_LIBRARY],
                file_path=MP3_FILE,
            )

    @staticmethod
    def test_django_file_validator_when_library_is_python_magic_library():
        """
        test django file validator when the library is python magic libraries
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT["mime"],
            acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=[PYTHON_MAGIC],
            file_path=JPEG_FILE,
        )
        current_file = result_of_validation["python_magic"]
        assert current_file["status"] == OK
        assert current_file["file_name"] == JPEG_OBJECT["name"]
        assert current_file["file_mime"] == JPEG_OBJECT["mime"]
        assert current_file["file_type"] == JPEG_OBJECT["type"]
        assert current_file["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_django_file_validator_when_library_is_pure_magic_library():
        """
        test django file validator when library is pure magic library
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT["mime"],
            acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=[PURE_MAGIC],
            file_path=JPEG_FILE,
        )
        current_file = result_of_validation["pure_magic"]
        assert current_file["status"] == OK
        assert current_file["file_name"] == JPEG_OBJECT["name"]
        assert current_file["file_mime"] == JPEG_OBJECT["mime"]
        assert current_file["file_type"] == JPEG_OBJECT["type"]
        assert current_file["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_django_file_validator_when_library_is_file_type_library():
        """
        test django file validator when the library is file type libraries
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT["mime"],
            acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=[FILETYPE],
            file_path=JPEG_FILE,
        )

        current_file = result_of_validation[FILETYPE]
        assert current_file["status"] == OK
        assert current_file["file_name"] == JPEG_OBJECT["name"]
        assert current_file["file_mime"] == JPEG_OBJECT["mime"]
        assert current_file["file_type"] == JPEG_OBJECT["type"]
        assert current_file["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_django_file_validator_when_library_is_mimetypes_library():
        """

        :return:
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT["mime"],
            acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=[MIMETYPES],
            file_path=JPEG_FILE,
        )

        current_file = result_of_validation[MIMETYPES]
        assert current_file["status"] == OK
        assert current_file["file_name"] == JPEG_OBJECT["name"]
        assert current_file["file_mime"] == JPEG_OBJECT["mime"]
        assert current_file["file_type"] == JPEG_OBJECT["type"]
        assert current_file["file_extension"] == JPEG_OBJECT["extension"]

    @staticmethod
    def test_django_file_validator_when_library_is_default_library():
        """
        test django file validator when the library is the default library
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=MP3_OBJECT["mime"],
            acceptable_mimes=[MP3_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=[DEFAULT],
            file_path=MP3_FILE,
        )
        current_file = result_of_validation[DEFAULT]
        assert current_file["status"] == OK
        assert current_file["file_name"] == MP3_OBJECT["name"]
        assert current_file["file_mime"] == MP3_OBJECT["mime"]
        assert current_file["file_type"] == MP3_OBJECT["type"]
        assert current_file["file_extension"] == MP3_OBJECT["extension"]

    @staticmethod
    def test_django_file_validator_when_selected_all_library():
        """
        test django file validator when selected all libraries
        """
        result_of_validation = file_validator_by_django(
            content_type_guessed_by_django=JPEG_OBJECT["mime"],
            acceptable_mimes=[PNG_OBJECT["mime"], JPEG_OBJECT["mime"]],
            libraries=ALL_SUPPORTED_LIBRARIES,
            file_path=JPEG_FILE,
        )
        validation_data_django = result_of_validation[DEFAULT]
        assert validation_data_django["status"] == OK
        assert validation_data_django["file_name"] == JPEG_OBJECT["name"]
        assert validation_data_django["file_mime"] == JPEG_OBJECT["mime"]
        assert validation_data_django["file_type"] == JPEG_OBJECT["type"]
        assert validation_data_django["file_extension"] == JPEG_OBJECT["extension"]

        validation_data_python_magic = result_of_validation[PYTHON_MAGIC]
        assert validation_data_python_magic["status"] == OK
        assert validation_data_python_magic["file_name"] == JPEG_OBJECT["name"]
        assert validation_data_python_magic["file_mime"] == JPEG_OBJECT["mime"]
        assert validation_data_python_magic["file_type"] == JPEG_OBJECT["type"]
        assert (
            validation_data_python_magic["file_extension"] == JPEG_OBJECT["extension"]
        )

        validation_data_pure_magic = result_of_validation[PURE_MAGIC]
        assert validation_data_pure_magic["status"] == OK
        assert validation_data_pure_magic["file_name"] == JPEG_OBJECT["name"]
        assert validation_data_pure_magic["file_mime"] == JPEG_OBJECT["mime"]
        assert validation_data_pure_magic["file_type"] == JPEG_OBJECT["type"]
        assert validation_data_pure_magic["file_extension"] == JPEG_OBJECT["extension"]

        validation_data_filetype = result_of_validation[FILETYPE]
        assert validation_data_filetype["status"] == OK
        assert validation_data_filetype["file_name"] == JPEG_OBJECT["name"]
        assert validation_data_filetype["file_mime"] == JPEG_OBJECT["mime"]
        assert validation_data_filetype["file_type"] == JPEG_OBJECT["type"]
        assert validation_data_filetype["file_extension"] == JPEG_OBJECT["extension"]

        validation_data_mimetypes = result_of_validation[MIMETYPES]
        assert validation_data_mimetypes["status"] == OK
        assert validation_data_mimetypes["file_name"] == JPEG_OBJECT["name"]
        assert validation_data_mimetypes["file_mime"] == JPEG_OBJECT["mime"]
        assert validation_data_mimetypes["file_type"] == JPEG_OBJECT["type"]
        assert validation_data_mimetypes["file_extension"] == JPEG_OBJECT["extension"]


class TestfileValidatorByType:
    """
    tests for file_validator_by_type function
    """

    @staticmethod
    def test_file_validator_by_type_when_type_is_not_supported():
        """
        test for file_validator_by_type when type is not supported
        """
        with pytest.raises(TypeNotSupportedException):
            file_validator_by_type(acceptable_types=["test_type"], file_path=PNG_FILE)

    @staticmethod
    def test_file_validator_by_type_when_return_file_validation_exception():
        """
        test for file_validator_by_type when return file validation exception
        """
        with pytest.raises(FileValidationException):
            file_validator_by_type(acceptable_types=[VIDEO, AUDIO], file_path=PNG_FILE)

    @staticmethod
    def test_file_validator_by_type_when_return_validation_data_and_file_is_valid():
        """
        test for file_validator_by_type when return validation data and file is valid
        """
        result_of_validation = file_validator_by_type(
            acceptable_types=[IMAGE, AUDIO], file_path=PNG_FILE,
        )
        assert result_of_validation["status"] == OK
        assert result_of_validation["library"] == FILETYPE
        assert result_of_validation["file_name"] == PNG_OBJECT["name"]


class TestValidatedFileField:
    """
    tests for ValidatedFileField
    """

    @staticmethod
    def test_when_file_is_valid_and_return_none():
        """
        test ValidatedFileField when file is valid and return none
        """
        new_instance = TestFileModel(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_when_file_is_not_valid_and_raise_validation_error():
        """
        test ValidatedFileField when file is not valid and raise validation error
        """
        new_instance = TestFileModel(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT["name"],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT["mime"],
            ),
        )

        with pytest.raises(ValidationError):
            new_instance.full_clean()

    @staticmethod
    def test_deconstruct_method():
        """
        test deconstruct method
        """
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
    def test_acceptable_mimes_is_none():
        """
        test acceptable mimes in ValidatedFileField is none
        """
        with pytest.raises(MimesEmptyException):

            class _TestFileMimeModel(models.Model):
                test_file = ValidatedFileField(
                    libraries=[ALL],
                    max_upload_file_size=1000000,
                )

    @staticmethod
    def test_libraries_is_none():
        """
        the test ValidatedFileField library is none
        """
        _my_field_instance = TestFileModelWithoutLibraries(
            test_file=get_tmp_file(
                file_name=JPEG_OBJECT["name"],
                file_path=JPEG_FILE,
                file_mime_type=JPEG_OBJECT["mime"],
            ),
        )


class TestFileSizeValidator:
    """
    test file size validator
    """

    @staticmethod
    def test_file_size_is_valid():
        """
        test file size is valid
        """
        new_instance = TestFileModelWithFileSizeValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_file_size_is_not_valid():
        """
        test file size is not valid
        """
        with pytest.raises(ValidationError):
            new_instance = TestFileModelWithFileSizeValidatorNotValidSize(
                test_file=get_tmp_file(
                    file_name=PNG_OBJECT["name"],
                    file_path=PNG_FILE,
                    file_mime_type=PNG_OBJECT["mime"],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_max_upload_file_size_is_none():
        """
        test max upload file size is none
        """
        with pytest.raises(SizeValidationException):

            class _TestFileModelWithFileValidatorNotMaxUploadSize(models.Model):
                test_file = models.FileField(validators=[FileSizeValidator()])

    @staticmethod
    def test_eq_method():
        """
        test eq method
        """
        file_validator_one = FileSizeValidator(max_upload_file_size=10485760)
        file_validator_two = FileSizeValidator(max_upload_file_size=10485760)
        assert file_validator_one == file_validator_two


class TestFileValidator:
    """
    test for file validator
    """

    @staticmethod
    def test_when_file_is_valid_and_return_none():
        """
        test when file is valid and return none
        """
        new_instance = TestFileModelWithFileValidator(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_when_file_is_not_valid_and_return_none():
        """
        test when file is not valid and return none
        """
        with pytest.raises(ValidationError):
            new_instance = TestFileModelWithFileValidator(
                test_file=get_tmp_file(
                    file_name=JPEG_OBJECT["name"],
                    file_path=JPEG_FILE,
                    file_mime_type=JPEG_OBJECT["mime"],
                ),
            )

            new_instance.full_clean()

    @staticmethod
    def test_when_file_size_is_none():
        """
        test when file size is none
        """
        new_instance = TestFileModelWithFileValidatorSizeIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_when_libraries_is_none():
        """
        test when libraries is none
        """
        new_instance = TestFileModelWithFileValidatorLibraryIsNone(
            test_file=get_tmp_file(
                file_name=PNG_OBJECT["name"],
                file_path=PNG_FILE,
                file_mime_type=PNG_OBJECT["mime"],
            ),
        )

        new_instance.full_clean()

    @staticmethod
    def test_when_libraries_is_not_supported():
        """
        test when libraries is not supported
        """
        with pytest.raises(LibraryNotSupportedException):

            class _TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                """
                Test Model
                """

                test_file = models.FileField(
                    validators=[
                        FileValidator(
                            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]],
                            libraries=[BAD_OBJECT["name"]],
                        ),
                    ],
                )

    @staticmethod
    def test_when_acceptable_mimes_is_none():
        """
        test when acceptable mimes is none
        """
        with pytest.raises(MimesEmptyException):

            class _TestFileModelWithFileValidatorNotSupportedLibrary(models.Model):
                """
                Test Model
                """

                test_file = models.FileField(validators=[FileValidator()])

    @staticmethod
    def test_eq_methode():
        """
        test eq methode
        """
        file_validator_one = FileValidator(
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]], libraries=[ALL],
        )
        file_validator_two = FileValidator(
            acceptable_mimes=[PNG_OBJECT["mime"], MP3_OBJECT["mime"]], libraries=[ALL],
        )
        assert file_validator_one == file_validator_two


class TestGuessTheType:
    """
    test for guess_the_type function in utils.py
    """

    @staticmethod
    def test_guess_the_type_function_when_file_is_invalid_and_return_none():
        """
        test guess the type function when file is invalid and return none
        """
        file_type = guess_the_type(file_path=BAD_FILE)
        assert file_type is None

    @staticmethod
    def test_guess_the_type_function_when_file_is_archive():
        """
        test guess the type function when file is archive
        """
        file_type = guess_the_type(file_path=ZIP_FILE)
        assert file_type is ARCHIVE

    @staticmethod
    def test_guess_the_type_function_when_file_is_image():
        """
        test guess the type function when file is image
        """
        file_type = guess_the_type(file_path=PNG_FILE)
        assert file_type is IMAGE

    @staticmethod
    def test_guess_the_type_function_when_file_is_video():
        """
        test guess the type function when file is video
        """
        file_type = guess_the_type(file_path=MP4_FILE)
        assert file_type is VIDEO

    @staticmethod
    def test_guess_the_type_function_when_file_is_audio():
        """
        test guesses the type function when file is audio
        """
        file_type = guess_the_type(file_path=MP3_FILE)
        assert file_type is AUDIO

    @staticmethod
    def test_guess_the_type_function_when_file_is_font():
        """
        test guess the type function when file is font
        """
        file_type = guess_the_type(file_path=TTF_FILE)
        assert file_type is FONT


class TestException:
    """
    test
    """

    @staticmethod
    def test_error_message_function_return_correct_message():
        """
        We test whether this error message function returns the expected message or not
        """
        message = error_message(
            message=TEMPLATE_EXPECTED_MESSAGE,
            file_name=PNG_OBJECT["name"],
            file_size="20 MB",
            mimes=["image/png", "audio/mpeg"],
            max_file_size="10 MB",
            current_file_mime=PNG_OBJECT["mime"],
        )
        assert EXPECTED_MESSAGE in message


def test_file_validator_when_file_is_valid(jpeg=JPEG_FILE):
    """
    :param jpeg: It is a fixture for jpeg files
    :return: The result we expect to return is None, which means that everything is OK
    """
    result_of_validation = file_validator(JPEG_OBJECT["mime"], file_path=jpeg)

    validation_data_python_magic = result_of_validation[PYTHON_MAGIC]
    assert validation_data_python_magic["status"] == OK
    assert validation_data_python_magic["file_name"] == JPEG_OBJECT["name"]
    assert validation_data_python_magic["file_mime"] == JPEG_OBJECT["mime"]
    assert validation_data_python_magic["file_type"] == JPEG_OBJECT["type"]
    assert validation_data_python_magic["file_extension"] == JPEG_OBJECT["extension"]

    validation_data_pure_magic = result_of_validation[PURE_MAGIC]
    assert validation_data_pure_magic["status"] == OK
    assert validation_data_pure_magic["file_name"] == JPEG_OBJECT["name"]
    assert validation_data_pure_magic["file_mime"] == JPEG_OBJECT["mime"]
    assert validation_data_pure_magic["file_type"] == JPEG_OBJECT["type"]
    assert validation_data_pure_magic["file_extension"] == JPEG_OBJECT["extension"]

    validation_data_filetype = result_of_validation[FILETYPE]
    assert validation_data_filetype["status"] == OK
    assert validation_data_filetype["file_name"] == JPEG_OBJECT["name"]
    assert validation_data_filetype["file_mime"] == JPEG_OBJECT["mime"]
    assert validation_data_filetype["file_type"] == JPEG_OBJECT["type"]
    assert validation_data_filetype["file_extension"] == JPEG_OBJECT["extension"]

    validation_data_mimetypes = result_of_validation[MIMETYPES]
    assert validation_data_mimetypes["status"] == OK
    assert validation_data_mimetypes["file_name"] == JPEG_OBJECT["name"]
    assert validation_data_mimetypes["file_mime"] == JPEG_OBJECT["mime"]
    assert validation_data_mimetypes["file_type"] == JPEG_OBJECT["type"]
    assert validation_data_mimetypes["file_extension"] == JPEG_OBJECT["extension"]


def test_size_validator():
    """
    :return:
    """
    with pytest.raises(SizeValidationException):
        assert size_validator(max_upload_file_size=1, file_path=PNG_FILE)


def test_all_mimes_is_equal():
    """
    test all_mimes_is_equal function in utils.py
    """

    assert all_mimes_is_equal(["image/png"]) is False
