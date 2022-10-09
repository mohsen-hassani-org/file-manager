from .exceptions import DirectoryDoesntHaveSizeAttribute, DirectoryDoesntHaveTypeAttribute, FileDoesntHaveContentAttribute


class SerializerPathInfoMixin:
    def __init__(self, path_info=None, data=..., **kwargs):
        if path_info is not None:
            data = self._create_data_from_path_info(path_info)
        super().__init__(data, **kwargs)

    def _create_data_from_path_info(self, path_info):
        return {
            'full_path': path_info._path,
            'path_type': path_info.path_type,
            'file_name': path_info.file_name,
            'file_extension': path_info.file_extension,
            'file_size': path_info.file_size,
            'contents': path_info.contents,
            'created_at': path_info.created_at,
            'last_modified': path_info.last_modified,
        }

