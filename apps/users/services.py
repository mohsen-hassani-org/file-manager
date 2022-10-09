import os
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apps.core.base import AbstractService
from .models import User
from .exceptions import UserDirectoryAlreadyExists


class RegisterUserService(AbstractService):
    id = None
    email = None
    password = None
    first_name = None
    last_name = None

    def execute(self):
        user = self._create_user()
        try:
            self._create_user_folder(user)
        except UserDirectoryAlreadyExists:
            pass
        return user

    def _create_user(self):
        user = User.objects.create_user(
            id=self.id,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        return user

    def _create_user_folder(self, user):
        base_dir = settings.BASE_DIR
        directory_name = f'user_{user.id}'
        user_dir = os.path.join(base_dir, settings.FILE_MANAGER_BASE_PATH, directory_name)
        try:
            os.mkdir(user_dir)
        except FileExistsError as ex:
            raise UserDirectoryAlreadyExists() from ex