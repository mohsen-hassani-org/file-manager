import os
import shutil
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from apps.files.path_info import PathTypes
from apps.users.services import RegisterUserService
from rest_framework.test import force_authenticate
from ..views import NewDirectoryAPI, PathInfoAPI, RootInfoAPI
from ..services import NewDirectoryService
from ..exceptions import DirecotryAlreadyExistsException


UNREACHABLE_USER_ID = 99999999


class RootInfoAPITests(APITestCase):
    def setUp(self):
        service = RegisterUserService(
            id=UNREACHABLE_USER_ID,
            email='dummy@mail.com',
            password='abcABC123!@#',
            first_name='Dum',
            last_name='My'
        )
        self.user = service.execute()

    def tearDown(self) -> None:
        shutil.rmtree(self.user.user_base_directory)

    def test_root_info_returns_empty_list_of_PathInfo_for_newly_register_users(self):
        factory = APIRequestFactory()
        url = reverse('file:root_files')
        request = factory.get(url)
        force_authenticate(request, self.user)
        view = RootInfoAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('contents')), 0)

    def test_root_info_has_all_expected_fields(self):
        factory = APIRequestFactory()
        url = reverse('file:root_files')
        request = factory.get(url)
        force_authenticate(request, self.user)
        view = RootInfoAPI.as_view()
        response = view(request)
        expected_fields = [
            'full_path', 'path_type', 'file_name', 'file_extension',
            'file_size', 'created_at', 'last_modified', 'contents'
        ]
        self.assertTrue(all(field in response.data.keys() for field in expected_fields))

    def test_root_info_path_type_is_dir(self):
        factory = APIRequestFactory()
        url = reverse('file:root_files')
        request = factory.get(url)
        force_authenticate(request, self.user)
        view = RootInfoAPI.as_view()
        response = view(request)
        path_type = response.data.get('path_type')
        self.assertEqual(path_type, PathTypes.DIRECTORY.value)

    def test_root_info_path_type_in_DIR_or_FILE(self):
        factory = APIRequestFactory()
        url = reverse('file:root_files')
        request = factory.get(url)
        force_authenticate(request, self.user)
        view = RootInfoAPI.as_view()
        response = view(request)
        path_type = response.data.get('path_type')
        self.assertIn(path_type, [path_type.value for path_type in PathTypes])
        


class PathInfoAPITests(APITestCase):
    def setUp(self):
        self.user = RegisterUserService(
            id=UNREACHABLE_USER_ID,
            email='dummy@mail.com',
            password='abcABC123!@#',
            first_name='Dum',
            last_name='My'
        ).execute()

    def tearDown(self) -> None:
        shutil.rmtree(self.user.user_base_directory)


class NewDirectoryAPITests(APITestCase):
    def setUp(self):
        self.user = RegisterUserService(
            id=UNREACHABLE_USER_ID,
            email='dummy@mail.com',
            password='abcABC123!@#',
            first_name='Dum',
            last_name='My'
        ).execute()

    def tearDown(self) -> None:
        shutil.rmtree(self.user.user_base_directory)
    
    def test_new_directory_api_calls_new_directory_service(self):
        factory = APIRequestFactory()
        kwargs = {'path': '/'}
        url = reverse('file:new_directory', kwargs=kwargs)
        request = factory.post(url, data={
            'directory_name': 'new_dir2'
        })
        force_authenticate(request, self.user)
        view = NewDirectoryAPI.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(DirecotryAlreadyExistsException):
            NewDirectoryService(path=self.user.user_base_directory, new_directory_name='new_dir2').execute()

    def test_view_join_user_base_directory_and_user_current_directory(self):
        NewDirectoryService(path=self.user.user_base_directory, new_directory_name='new_dir3').execute()
        kwargs = {'path': 'new_dir3'}
        factory = APIRequestFactory()
        url = reverse('file:new_directory', kwargs=kwargs)
        request = factory.post(url, data={
            'directory_name': 'new_dir4'
        })
        force_authenticate(request, self.user)
        view = NewDirectoryAPI.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_path = os.path.join(self.user.user_base_directory, 'new_dir3/new_dir4')
        self.assertTrue(os.path.exists(final_path))

    def test_new_directory_returns_400_if_directory_already_exists(self):
        factory = APIRequestFactory()
        kwargs = {'path': '/'}
        url = reverse('file:new_directory', kwargs=kwargs)
        request = factory.post(url, data={'directory_name': 'new_dir5'})
        force_authenticate(request, self.user)
        view = NewDirectoryAPI.as_view()
        response1 = view(request, **kwargs)
        response2 = view(request, **kwargs)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

       

       