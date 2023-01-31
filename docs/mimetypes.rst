====================
MimeTypes Library
====================

The good news is that we also support the native Python library, `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_, and you can add it to your project as follows:

.. code-block:: console

    $ from file_validator.validators import file_validator_by_mimetypes

For the mimetypes library, you must do exactly as above:


**Example** : 👇


.. code-block:: python

    from file_validator.validators import file_validator_by_mimetypes

    file_validator_by_mimetypes(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')


.. autofunction:: file_validator.validators.file_validator_by_mimetypes

