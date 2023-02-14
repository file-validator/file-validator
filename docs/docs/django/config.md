---
sidebar_position: 1
---

# Config

You should add the following `FILE_UPLOAD_HANDLERS` settings to your django project `settings.py`:

```jsx title="settings.py"
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]
```

add the app to `INSTALLED_APPS` :

```jsx title="settings.py"
INSTALLED_APPS = [
    'file_validator',
]
```
