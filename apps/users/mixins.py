from os import path
from django.conf import settings

class UserFileManagerMixin:
    @property
    def user_base_directory(self):
        base_dir = settings.FILE_MANAGER_BASE_PATH 
        return path.join(base_dir, f'user_{self.id}')