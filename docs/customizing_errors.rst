====================
Customizing Errors
====================

It is possible that you can customize the error messages,
that is, show the format of the files or mimes in the error
message, you can do this in the following way:


First, in your Django settings (``settings.py``), you must specify the error message as follows:

.. code-block:: python

    FILE_VALIDATOR_ERROR_MESSAGE = "{file} is not valid"

To display the current file name in the error message, you must put the ``{file}`` string in your error message
for example : 👇

.. code-block:: python

    FILE_VALIDATOR_ERROR_MESSAGE = "{file} Your custom error message"


To display the mimes based on which the file is to be validated,
you must include ``{mimes}`` string in your error message.
for example : 👇


.. code-block:: python

    FILE_VALIDATOR_ERROR_MESSAGE = "{mimes} Your custom error message"


To display both ``memes`` and ``file name``, you can put both in your error message.
for example : 👇

.. code-block:: python

    FILE_VALIDATOR_ERROR_MESSAGE = "{file} and {mimes} Your custom error message"



.. autofunction:: file_validator.exceptions.error_message
