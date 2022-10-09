import os
from apps.core.base import AbstractService
from .path_info import PathInfo
from .exceptions import DirecotryAlreadyExistsException
from .utils import clean_path


class PathAbstractService(AbstractService):
    path = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_info = PathInfo(self.path)


class InfoService(PathAbstractService):
    def execute(self):
        """Get details of the path, including its sub-files

        Returns:
            PathInfo: Information of the path
        """
        return self.path_info


class DeleteService(PathAbstractService):
    pass


class NewDirectoryService(PathAbstractService):
    new_directory_name = None
    
    def execute(self):
        directory_name = clean_path(self.new_directory_name)
        new_path = os.path.join(self.path_info.full_path, directory_name)
        if os.path.exists(new_path):
            raise DirecotryAlreadyExistsException()
        os.mkdir(new_path)
        return PathInfo(new_path)
        


class NewFileService(PathAbstractService):
    new_file_path = None


class MoveService(PathAbstractService):
    destination_path = None


class CopyService(PathAbstractService):
    destination_path = None

