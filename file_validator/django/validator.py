from django.core.exceptions import ValidationError
from filetype import (
    get_type,
    is_extension_supported,
    match,
    guess,
    is_audio,
    is_video,
    is_font,
    is_image,
    is_archive,
)
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator:
    """ """
    def __init__(self, *args):
        """
        :param args: You can choose different types and pass it as a string and be sure to separate the types with commas, example : FileValidator("mp3", "avi")

        :raises ValueError: If the type you enter is not supported, it will cause this value error, please check that there are no typos, and you can check the list of supported types from the documentation.
        """
        selected_types = {}
        for selected_file_type in args:
            if is_extension_supported(selected_file_type):
                file_object = get_type(ext=selected_file_type)
                selected_types.update(
                    {
                        selected_file_type: file_object,
                    }
                )
            else:
                raise ValueError(
                    f"{selected_file_type} Is Not Valid, Please Visit Documentation And Enter Valid Type"
                )
        self.selected_types = selected_types

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        :return: If everything is ok, the permission to upload the file will be given, otherwise, a validation error will be returned
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        result_validation = []
        current_file = guess(file_path)
        if current_file is not None:
            for file_extension, temporary_file in self.selected_types.items():
                if (
                    current_file.EXTENSION != file_extension
                    and current_file.MIME != temporary_file.MIME
                ):
                    result_validation.append(True)
                elif (
                    current_file.EXTENSION == file_extension
                    and current_file.MIME == temporary_file.MIME
                ):
                    result_validation.append(False)
        else:
            raise ValidationError("Please Upload a Valid File")

        file_is_not_valid = all(result_validation)
        if file_is_not_valid:
            raise ValidationError(
                f"{current_file.extension} File Is Not Valid, Please Upload a valid Type"
            )
