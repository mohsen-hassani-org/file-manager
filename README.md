# File Manager
A simple API for managing files in cloud

## Requirements
 - python3
 - pipenv

## Installation

```sh
git clone https://github.com/mohsen-hassani-org/file-manager.git
cd file-manager
cp .env.example .env # CHANGE THIS FILE ACCORDING TO YOUR PROJECT
pipenv install
python3 manage.py runserver
```

## Endpoints
    [x] /api/v1/files/                         => my all files in root
    [x] /api/v1/files/<path>/                  => details of a path (including subfiles in case of directory) 
    [ ] /api/v1/files/info/<path>/             => download a file or raise in case of directory
    [ ] /api/v1/files/download/<path>/         => download a file or raise in case of directory
    [ ] /api/v1/files/delete/<path>/           => delete a file or raise in case of directory
    [x] /api/v1/files/new-directory/<path>/    => new directory in this path or raise error in case of folder
    [ ] /api/v1/files/upload/<path>/           => upload new file here
    [ ] /api/v1/files/move/<path>/             => upload new file here