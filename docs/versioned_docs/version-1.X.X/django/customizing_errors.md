---
sidebar_position: 5
---

# Customizing Errors

It is possible that you can customize the error messages, that is, show the format of the files or mimes in the error message, you can do this in the following way:

First, in your Django settings `settings.py`, you must specify the error message as follows:
```
FILE_VALIDATOR_ERROR_MESSAGE = "{current_file_name} is not valid"
```
To display the current file name in the error message, you must put the `{current_file_name}` string in your error message for example : 👇
```
FILE_VALIDATOR_ERROR_MESSAGE = "{current_file_name} Your custom error message"
```
To display the mimes based on which the file is to be validated, you must include `{acceptable_mimes}` string in your error message. for example : 👇
```
FILE_VALIDATOR_ERROR_MESSAGE = "{acceptable_mimes} Your custom error message"
```
To display both mimes and file name, you can put both in your error message. for example : 👇
```
FILE_VALIDATOR_ERROR_MESSAGE = "{current_file_name} and {acceptable_mimes} Your custom error message"
```

:::info

> In this section we will explain the parameters you can use in your message message

| Parameters                 | Description                                           |
|----------------------------|:------------------------------------------------------|
| `{current_file_name}`      | return the current file name                          |
| `{current_file_size}`      | return the current file size                          |
| `{current_file_mime}`      | return the current file mime                          |
| `{current_file_type}`      | return the current file type                          |
| `{current_file_extension}` | return the current file extension                     |
| `{acceptable_mimes}`       | return the accepted mime                              |
| `{acceptable_types}`       | return the accepted type                              |
| `{acceptable_extensions}`  | return the accepted extension                         |
| `{max_file_size}`          | return the Maximum file size that the user can upload |


:::
