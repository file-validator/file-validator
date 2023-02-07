"""
In this module, the constants used at the library level are defined
"""

PYTHON_MAGIC: str = "python_magic"
PURE_MAGIC: str = "pure_magic"
FILETYPE: str = "filetype"
MIMETYPES: str = "mimetypes"
DEFAULT: str = "default"
ALL: str = "all"
ALL_SUPPORTED_LIBRARIES: list = [
    PYTHON_MAGIC,
    PURE_MAGIC,
    FILETYPE,
    MIMETYPES,
    DEFAULT,
    ALL,
]
SELECTING_ALL_SUPPORTED_LIBRARIES: str = "all"
ZERO: int = 0
MIMES_EMPTY: str = "The args value is empty, please pass the value (file MIME)."
MIME_NOT_VALID: str = "mime is not a valid"
MIME_NOT_VALID_WITH_MIME_NAME: str = "{file_mime} is not valid"
FILE_IS_NOT_VALID: str = "{file} is not valid"
FILE_SIZE_IS_NOT_VALID: str = (
    "{file_size} is not valid size for this file, you can upload files up to {max_file_size}."
)
MIMES_IS_EQUAL: str = "The mimes ({mimes}) are similar, please use different mimes"
LIBRARY_IS_NOT_SUPPORTED: str = (
    "{library} is not supported, you can choice library from this list : {libraries} "
)

DEFAULT_ERROR_MESSAGE: str = "{file} is not valid"
DEFAULT_FILE_NAME: str = 'file'
MAX_UPLOAD_SIZE_IS_EMPTY: str = 'max_upload_file_size is empty'
