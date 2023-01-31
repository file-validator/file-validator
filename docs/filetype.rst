====================
FileType Library
====================
filetype a Python package to infer file type and MIME type checking the magic numbers signature of a file or buffer.
we also support the `filetype <https://github.com/h2non/filetype.py>`_ library, and you can import it to your project as follows:

.. code-block:: python

    from file_validator.validators import file_validator_by_filetype

To use this function, just call the function like the previous example and give it the path of the file and the mimes you want the file to be validated based on.

**Example** : 👇


.. code-block:: python

    from file_validator.validators import file_validator_by_filetype

    file_validator_by_filetype(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')


.. autofunction:: file_validator.validators.file_validator_by_filetype


.. note::
    To see what types the filetype library supports,
    you can refer to the `link <https://github.com/h2non/filetype.py#supported-types>`_ below

