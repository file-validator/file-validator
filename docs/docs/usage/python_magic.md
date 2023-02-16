---
sidebar_position: 1
---

# Python Magic

[python-magic](https://github.com/ahupp/python-magic) is a Python interface to the libmagic file type identification library. libmagic identifies file types by checking their headers according to a predefined list of file types. This functionality is exposed to the command line by the Unix command file.

:::caution

Since the [python-magic](https://github.com/ahupp/python-magic)
library may treat audio files like mp3 as programs
or `application/octet-stream` and it’s a bit
annoying, I suggest when you want to validate
audio files from two libraries (**filetype**, **MimeTypes**, **pure magic**)
or use the safe mode method.
:::

If you want to use File Validators made using the [python-magic](https://github.com/ahupp/python-magic)
library, you should add it to your program as follows:

```python
from file_validator.validators import file_validator_by_python_magic
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator_by_python_magic

file_validator_by_python_magic(acceptable_mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters | Type           | Description     |
|-----------|:--------------|:------|
| file_path | `string` | The path to the file you want to validate  |
| acceptable_mimes     | `list`      | The mime of the files you want to validate based on them, example: image/png   |

| Returns:                                                                                                                             |
|:-------------------------------------------------------------------------------------------------------------------------------------|
| If everything is OK it will return information about file such `file name`, `file mime`, `file extensions` , otherwise it will return a `FileValidationException`. |ntio


:::
