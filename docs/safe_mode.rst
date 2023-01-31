====================
Safe Mode
====================
By using Safe Mode, you can perform validation
operations using all three libraries at the same time
To use, first import as in the example below:

.. code-block:: console

    from file_validator.validator import file_validator

Then just call the file_validator function:

.. code-block:: python

    from file_validator.validators import file_validator

    file_validator(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')

.. autofunction:: file_validator.validators.file_validator
