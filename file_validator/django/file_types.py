from filetype import types
"""
In this section, we receive the types of files using the
filetype library and store them as keys and values, where
the key contains the extension of the files and the value
is the type (object) of those files.
"""
FILE_TYPES = {}
for file_type in types:
    FILE_TYPES.update({file_type.EXTENSION.lower(): file_type})

