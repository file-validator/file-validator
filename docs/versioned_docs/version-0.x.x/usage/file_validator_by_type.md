---
sidebar_position: 5
---

# file validator by type

this file validator for validation of the overall type of files
        such `image`, `audio`, `video`, `archive`, `font`
```python
from file_validator.validators import file_validator_by_type
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator_by_type

file_validator_by_type(acceptable_types=['image'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters       | Type     | Description                                                             |
|------------------|:---------|:------------------------------------------------------------------------|
| file_path        | `string` | The path to the file you want to validate                               |
| acceptable_types | `list`   | acceptable types of file, Supported types `image`, `video`, `audio`, `archive`, `font` |

| Returns:                                                                                                                                         |
|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| If everything is OK it will return information about file such `file name`, `file type` , otherwise it will return a `FileValidationException`.                 |


:::

:::note

To see what types the filetype library supports, you can refer to the [link](https://github.com/h2non/filetype.py#supported-types) below
:::
