---
sidebar_position: 2
---

# Pure Magic


[puremagic](https://github.com/cdgriffith/puremagic) is a pure python module that will identify a file based off it's magic numbers.It is designed to be minimalistic and inherently cross platform compatible. It is also designed to be a stand in for python-magic, it incorporates the functions from_file(filename[, mime]) and from_string(string[, mime]) however the magic_file() and magic_string() are more powerful and will also display confidence and duplicate matches.

you can add it to your project as follows:

```python
from file_validator.validators import file_validator_by_pure_magic
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator_by_pure_magic

file_validator_by_pure_magic(acceptable_mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters | Type           | Description     |
|-----------|:--------------|:------|
| file_path | `string` | The path to the file you want to validate  |
| acceptable_mimes     | `list`      | The mime of the files you want to validate based on them, example: image/png   |

| Returns:|
|:----------|
| If everything is OK it will return information about file such `file name`, `file mime`, `file extensions` , otherwise it will return a ValueError. |


:::
