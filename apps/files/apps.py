import os
from django.apps import AppConfig
from django.conf import settings


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.files'

    def ready(self):
        self._create_user_files_base_directory()

    def _create_user_files_base_directory(self):
        absolute_path = os.path.join(settings.BASE_DIR, settings.FILE_MANAGER_BASE_PATH)
        if not os.path.exists(absolute_path):
            os.mkdir(absolute_path)

       

        