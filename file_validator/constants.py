"""In this module, the constants used at the library level are defined."""

PYTHON_MAGIC: str = "python_magic"
PURE_MAGIC: str = "pure_magic"
MIMETYPES: str = "mimetypes"
FILETYPE: str = "filetype"
DEFAULT: str = "default"
DJANGO: str = "django"
SIZE: str = "size"
ALL: str = "all"
ALL_SUPPORTED_LIBRARIES: list = [
    PYTHON_MAGIC,
    PURE_MAGIC,
    FILETYPE,
    MIMETYPES,
    DJANGO,
    ALL,
]
SELECTING_ALL_SUPPORTED_LIBRARIES: str = "all"
ZERO: int = 0
MIMES_EMPTY: str = "The args value is empty, please pass the value (file MIME)."
MIME_NOT_VALID: str = "mime is not a valid"
MIME_NOT_VALID_WITH_MIME_NAME: str = "{current_file_mime} is not valid"
FILE_IS_NOT_VALID: str = "{current_file_name} is not valid"
FILE_SIZE_IS_NOT_VALID: str = (
    "{current_file_name} is not valid, \n"
    "{current_file_size} is not valid size for this file, \n"
    "you can upload files up to {max_file_size}."
)
MIMES_IS_EQUAL: str = "The mimes ({mimes}) are similar, please use different mimes"
LIBRARY_IS_NOT_SUPPORTED: str = (
    "{library} is not supported, you can choice library from this list : {libraries} "
)

DEFAULT_ERROR_MESSAGE: str = (
    "{current_file_name} is not valid, \n"
    "acceptable mimes: {acceptable_mimes}, \n"
    "acceptable types: {acceptable_types}, \n"
    "acceptable extensions: {acceptable_extensions}, \n"
    "your file mime: {current_file_mime}, \n"
    "your file type: {current_file_type}, \n"
    "your file extension: {current_file_extension}"
)
ERROR_MESSAGE_FOR_MIME_VALIDATION: str = (
    "{current_file_name} is not valid, \n"
    "acceptable mimes: {acceptable_mimes}, \n"
    "your file mime: {current_file_mime}\n"
)
ERROR_MESSAGE_FOR_TYPE_VALIDATION: str = (
    "{current_file_name} is not valid, \n"
    "acceptable mimes: {acceptable_types}, \n"
    "your file mime: {current_file_type}\n"
)
ERROR_MESSAGE_FOR_EXTENSION_VALIDATION: str = (
    "{current_file_name} is not valid, \n"
    "acceptable extensions: {acceptable_extensions}, \n"
    "your file extension: {current_file_extension}\n"
)
DEFAULT_FILE_NAME: str = "file"
MAX_UPLOAD_SIZE_IS_EMPTY: str = "max_upload_file_size is empty"
OK: str = "ok"
FONT: str = "font"
AUDIO: str = "audio"
VIDEO: str = "video"
IMAGE: str = "image"
ARCHIVE: str = "archive"
SUPPORTED_TYPES: list = [AUDIO, VIDEO, IMAGE, ARCHIVE, FONT]
TYPE_NOT_SUPPORTED: str = (
    "The type you entered is not supported, List of"
    " supported types: font, audio, video, image, archive"
)
FILE_NOT_VALID: str = "file is not valid"
PARAMETERS_ARE_EMPTY: str = (
    "you must fill at least one acceptable_mimes or acceptable_types parameter"
)
FILE_EXTENSION_NOT_VALID: str = "{file_extension} is not valid"
