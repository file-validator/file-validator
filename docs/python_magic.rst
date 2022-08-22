====================
Python Magic Library
====================
python-magic is a Python interface to the libmagic file type identification
library. libmagic identifies file types by checking their headers according
to a predefined list of file types. This functionality is exposed to the
command line by the Unix command file.


.. warning::
    Since the `python-magic <https://github.com/ahupp/python-magic>`_ library may treat audio files
    like mp3 as programs or application/octet-stream and it's a bit
    annoying, I suggest when you want to validate audio files from
    two libraries (`filetype <https://github.com/h2non/filetype.py>`_, `MimeTypes <https://docs.python.org/3/library/mimetypes.html>`_) or use the safe mode method.



If you want to use File Validators made using the `python-magic <https://github.com/ahupp/python-magic>`_ library, you should add it to your program as follows:

.. code-block:: python

    from file_validator.validator import file_validator_by_python_magic

Just call this function and give the function path of the file and the mimes you want the files to be validated based on:


**Example** : 👇


.. code-block:: python

    from file_validator.validator import file_validator_by_python_magic

    file_validator_by_python_magic(mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')


.. autofunction:: file_validator.validator.file_validator_by_python_magic

