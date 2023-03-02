#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "humanize==4.4.0",
    "filetype==1.1.0",
    "termcolor==1.1.0",
    "puremagic==1.14",
    "python-dotenv==0.21.1",
    "django",
    "python-magic-bin==0.4.14 ; platform_system == 'Windows'",
    "python-magic==0.4.27 ; platform_system != 'Windows'"
]


test_requirements = [
    "pytest>=3",
]

setup(
    author="Reza Shakeri",
    author_email="rzashakeri@outlook.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries"
    ],
    description="Python validation library to validate files "
                "using type, mime, extension, magic numbers and size ✅",
    entry_points={
        "console_scripts": [
            "file_validator=file_validator.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=[
        "file_validator",
        "file",
        "validator",
        "image_validator",
        "audio_validator",
        "video_validator",
        "django"
    ],
    name="file_validator",
    packages=find_packages(include=["file_validator", "file_validator.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/file-validator/file-validator",
    version="0.3.3",
    zip_safe=False,
    project_urls={
        'Documentation': "https://file-validator.github.io/",
        'Homepage': "https://github.com/file-validator",
        "Issue tracker": "https://github.com/file-validator/file-validator/issues",
        "Release notes": "https://github.com/file-validator/file-validator/releases",
        'Source': "https://github.com/file-validator/file-validator",
        'Discussions': "https://github.com/orgs/file-validator/discussions",
        'History Of Changes': "https://file-validator.github.io/docs/history/",
    },
)
