---
sidebar_position: 4
---

# FileType

[filetype](https://github.com/h2non/filetype.py) a Python package to infer file type and MIME type checking the magic numbers signature of a file or buffer. we also support the filetype library, and you can import it to your project as follows:

```python
from file_validator.validators import file_validator_by_filetype
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator_by_filetype

file_validator_by_filetype(acceptable_mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters | Type           | Description     |
|-----------|:--------------|:------|
| file_path | `string` | The path to the file you want to validate  |
| acceptable_mimes     | `list`      | The mime of the files you want to validate based on them, example: image/png   |

| Returns:                                                                                                                                                                       |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| If everything is OK it will return information about file such `file name`, `file mime`,`file type`, `file extensions` , otherwise it will return a `FileValidationException`. |


:::

:::note

To see what types the filetype library supports, you can refer to the [link](https://github.com/h2non/filetype.py#supported-types) below
:::
