---
sidebar_position: 3
---

# MimeTypes

The good news is that we also support the native Python library, [mimetypes](https://docs.python.org/3/library/mimetypes.html) MimeTypes, and you can add it to your project as follows:


```python
from file_validator.validators import file_validator_by_mimetypes
```

Just call this function and give the function path of the file and the mimes
you want the files to be validated based on:

```python
from file_validator.validators import file_validator_by_mimetypes

file_validator_by_mimetypes(acceptable_mimes=['audio/mpeg', 'video/mp4'], file_path='/path/to/file')
```


:::info

> Description of the return value and the function parameters:

| Parameters | Type         | Description     |
|-----------|:-------------|:------|
| file_path | ```string``` | The path to the file you want to validate  |
| acceptable_mimes     | `list`       | The mime of the files you want to validate based on them, example: image/png   |

| Returns:|
|:----------|
| If everything is OK it will return information about file such `file name`, `file mime`, `file extensions` , otherwise it will return a ValueError. |


:::
