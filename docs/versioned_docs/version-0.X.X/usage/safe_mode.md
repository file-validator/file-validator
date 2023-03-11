---
sidebar_position: 6
---

# Safe Mode 🔒

By using Safe Mode, you can perform validation operations using all libraries at the same time To use, first import as in the example below:

```python
from file_validator.validators import file_validator
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator

file_validator(acceptable_mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters | Type           | Description     |
|-----------|:--------------|:------|
| file_path | `string` | The path to the file you want to validate  |
| acceptable_mimes     | `list`      | The mime of the files you want to validate based on them, example: image/png   |

| Returns:|
|:----------|
| If everything is OK it will return information about file such `file name`, `file mime`, `file extensions` , otherwise it will return a `FileValidationException`. |


:::

:::note

To see what types the filetype library supports, you can refer to the [link](https://github.com/h2non/filetype.py#supported-types) below
:::
