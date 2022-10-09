import os
import shutil
from django.conf import settings
from django.test import TestCase
from ..services import (
    InfoService, DeleteService, MoveService,
    CopyService, NewDirectoryService, NewFileService
)
from ..path_info import PathInfo


class InfoSerivceTest(TestCase):
    def setUp(self) -> None:
        tmp_base_dir = os.path.join(settings.BASE_DIR, 'tmp')
        self.tmp_path = tmp_base_dir
        try:
            os.mkdir(tmp_base_dir)
        except FileExistsError:
            pass

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_execute_returns_PathInfo(self):
        file_path = os.path.join(self.tmp_path, 'file')
        with open(file_path, 'w') as fin:
            fin.write('')
        service = InfoService(path=file_path)
        file_from_service =service.execute()
        self.assertEqual(file_from_service, PathInfo(file_path))


class NewDirectoryTests(TestCase):
    def setUp(self) -> None:
        tmp_base_dir = os.path.join(settings.BASE_DIR, 'tmp')
        self.tmp_path = tmp_base_dir
        try:
            os.mkdir(tmp_base_dir)
        except FileExistsError:
            pass

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_new_directory_service_creates_new_directory(self):
        service = NewDirectoryService(path=self.tmp_path, new_directory_name='new_dir1')
        service.execute()
        new_path = os.path.join(self.tmp_path, 'new_dir1')
        self.assertTrue(os.path.exists(new_path))
        
    def test_new_directory_service_returns_PathInfo_object(self):
        service = NewDirectoryService(path=self.tmp_path, new_directory_name='new_dir2')
        path_info = service.execute()
        self.assertIsInstance(path_info, PathInfo)

    def test_new_directory_service_cuase_non_empty_contens_for_parent_direcotry(self):
        path_info_before = PathInfo(self.tmp_path)
        self.assertEqual(path_info_before.total_contents, 0)
        service = NewDirectoryService(path=self.tmp_path, new_directory_name='new_dir3')
        service.execute()
        path_info_after = PathInfo(self.tmp_path)
        self.assertGreater(path_info_after.total_contents, 0)
        
        