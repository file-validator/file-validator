"""
In this module, the constants used at the library level are defined
"""
PYTHON_MAGIC = "python_magic"
PURE_MAGIC = "pure_magic"
FILETYPE = "filetype"
MIMETYPES = "mimetypes"
DEFAULT = "default"
ALL_SUPPORTED_LIBRARIES = [PYTHON_MAGIC, PURE_MAGIC, FILETYPE, MIMETYPES]
SELECTING_ALL_SUPPORTED_LIBRARIES = "all"
ZERO = 0
MIMES_EMPTY = "The args value is empty, please pass the value (file MIME)."
MIME_NOT_VALID = "mime is not a valid"
MIME_NOT_VALID_WITH_MIME_NAME = "{file_mime} is not valid"
FILE_IS_NOT_VALID = "{file} is not valid"
FILE_SIZE_IS_NOT_VALID = (
    "{file_size} is not valid size, you can upload files up to {max_file_size}."
)
MIMES_IS_EQUAL = "The mimes ({mimes}) are similar, please use different mimes"
LIBRARY_IS_NOT_SUPPORTED = (
    "{library} is not supported, you can choice library from this list : {libraries} "
)
