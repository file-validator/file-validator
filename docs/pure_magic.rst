====================
PureMagic Library
====================
`puremagic <https://github.com/cdgriffith/puremagic>`_ is a pure python module that will identify a file based off it's magic numbers.

.. code-block:: python

    from file_validator.validators import file_validator_by_pure_magic

To use this function, just call the function like the previous example and give it the path of the file and the mimes you want the file to be validated based on.

**Example** : 👇


.. code-block:: python

    from file_validator.validators import file_validator_by_pure_magic

    file_validator_by_pure_magic(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')


.. autofunction:: file_validator.validators.file_validator_by_pure_magic


