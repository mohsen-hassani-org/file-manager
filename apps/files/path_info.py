import os
from pathlib import Path
from enum import Enum
from .exceptions import (
    DirectoryDoesntHaveSizeAttribute,
    DirectoryDoesntHaveTypeAttribute,
    FileDoesntHaveContentAttribute
)


class PathTypes(Enum):
    FILE = 'file'
    DIRECTORY = 'dir'


class PathInfo:
    def __init__(self, path):
        self._path = path
        self.path_type = self._get_path_type()
        self.created_at = self._get_created_datetime()
        self.last_modified = self._get_last_modified()
        self.file_name, self.file_extension = self._get_file_name_and_extension()

    def __eq__(self, __o: 'PathInfo'):
        return self._path == __o._path

    def __repr__(self):
        return f'PathInfo(full_path={self._path})'

    def _get_path_type(self):
        path_type = PathTypes.FILE if os.path.isfile(self._path) else PathTypes.DIRECTORY
        return path_type.value

    def _get_created_datetime(self):
        current_path = Path(self._path)
        info = current_path.stat()
        return info.st_ctime
        
    def _get_last_modified(self):
        current_path = Path(self._path)
        info = current_path.stat()
        return info.st_mtime
        
    def _get_file_size(self):
        current_path = Path(self._path)
        info = current_path.stat()
        return info.st_size
        
    def _get_file_type(self):
        raise NotImplementedError()
        
    def _get_file_name_and_extension(self):
        path, full_name = os.path.split(self._path)
        name, extension = os.path.splitext(full_name)
        return full_name, extension

    @property
    def full_path(self):
        return self._path

    @property
    def file_size(self):
        if self.path_type == PathTypes.DIRECTORY.value:
            return None
        return self._get_file_size()

    @property
    def file_type(self):
        if self.path_type == PathTypes.DIRECTORY.value:
            return None
        return self._get_file_type()

    @property
    def contents(self):
        if self.path_type == PathTypes.FILE.value:
            raise FileDoesntHaveContentAttribute
        with os.scandir(self._path) as entries:
            for entry in entries:
                path = os.path.join(self._path, entry.name)
                yield PathInfo(path)
                
    @property
    def total_contents(self):
        if self.path_type == PathTypes.FILE.value:
            return None
        return len(os.listdir(self._path))
    

