Size Validator
--------------
You can use the following function to validate the file size:

.. code-block:: python

    from file_validator.validators import size_validator

To use this function, just call the function like the previous example and give it the path of the file and the mimes you want the file to be validated based on.

**Example** : 👇


.. code-block:: python

    from file_validator.validators import size_validator

    size_validator(
        file_path = "/path/to/file",
        max_upload_file_size = 10485760
    )


.. autofunction:: file_validator.validators.file_validator_by_pure_magic


