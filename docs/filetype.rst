====================
FileType Library
====================

we also support the `filetype <https://github.com/h2non/filetype.py>`_ library, and you can import it to your project as follows:

.. code-block:: python

    from file_validator.validator import file_validator_by_filetype

To use this function, just call the function like the previous example and give it the path of the file and the mimes you want the file to be validated based on.

**Example** : 👇


.. code-block:: python

    from file_validator.validator import file_validator_by_filetype

    file_validator_by_filetype('audio/mpeg', 'video/mp4', file_path='/path/to/file')


.. autofunction:: file_validator.validator.file_validator_by_filetype
