import os
from datetime import timedelta
from django.test import TestCase
from django.conf import settings
from ..models import User
from ..services import RegisterUserService


# class ActivateUserServiceTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='dummy@mail.com',
#             password='P@ssw0rd'
#         )

#     def test_user_can_activate(self):
#         self.assertFalse(self.user.is_active)
#         service = ActivateUserService(key=self.user.activation_key)
#         service.execute()
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.is_active)

#     def test_wrong_key_raise_exception(self):
#         self.assertFalse(self.user.is_active)
#         service = ActivateUserService(key="WRONG_KEY")
#         with self.assertRaises(InvalidActivationKey):
#             service.execute()
#         self.user.refresh_from_db()
#         self.assertFalse(self.user.is_active)

#     def test_expired_key_raise_exception(self):
#         self.assertFalse(self.user.is_active)
#         self.user.created_at = self.user.created_at - (settings.USER_ACTIVATION_EXPIRATION + timedelta(minutes=1))
#         self.user.save()
#         service = ActivateUserService(key=self.user.activation_key)
#         with self.assertRaises(InvalidActivationKey):
#             service.execute()
#         self.user.refresh_from_db()
#         self.assertFalse(self.user.is_active)

#     def test_not_expired_key_activate_user(self):
#         self.assertFalse(self.user.is_active)
#         self.user.created_at = self.user.created_at - (settings.USER_ACTIVATION_EXPIRATION - timedelta(minutes=1))
#         self.user.save()
#         service = ActivateUserService(key=self.user.activation_key)
#         service.execute()
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.is_active)


class UserDirectoryServiceTest(TestCase):
    def setUp(self):
        self.email = 'dummy@mail.com'
        self.password = 'P@ssw0rd'
        self.first_name = 'FDummy'
        self.last_name = 'LDummy'

    def test_registered_user_has_base_folder(self):
        service = RegisterUserService(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        user = service.execute()
        base_dir = settings.BASE_DIR
        directory_name = f'user_{user.id}'
        user_dir = os.path.join(base_dir, settings.FILE_MANAGER_BASE_PATH, directory_name)
        self.assertTrue(os.path.exists(user_dir))


