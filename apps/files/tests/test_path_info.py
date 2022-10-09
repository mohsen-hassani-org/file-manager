import os
import shutil
from datetime import datetime
from time import time
from django.test import TestCase
from django.conf import settings
from ..path_info import PathInfo, PathTypes
from ..exceptions import DirectoryDoesntHaveSizeAttribute, DirectoryDoesntHaveTypeAttribute


class PathInfoTests(TestCase):
    def setUp(self) -> None:
        tmp_base_dir = os.path.join(settings.BASE_DIR, 'tmp')
        self.tmp_path = tmp_base_dir
        try:
            os.mkdir(tmp_base_dir)
        except FileExistsError:
            pass

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_path)

    def test_get_path_type(self):
        file_path = os.path.join(self.tmp_path, 'file')
        with open(file_path, 'w') as fin:
            fin.write('')
        file = PathInfo(file_path)
        self.assertEqual(file.path_type, PathTypes.FILE.value)
        self.assertNotEqual(file.path_type, PathTypes.DIRECTORY.value)

        dir_path = os.path.join(self.tmp_path, 'dir')
        os.mkdir(dir_path)
        dir = PathInfo(dir_path)
        self.assertEqual(dir.path_type, PathTypes.DIRECTORY.value)
        self.assertNotEqual(dir.path_type, PathTypes.FILE.value)

    def test_created_at(self):
        path = os.path.join(self.tmp_path, 'dir1')
        now = time()
        os.mkdir(path)
        dir = PathInfo(path)
        self.assertAlmostEqual(now, dir.created_at, delta=1)

    def test_file_size(self):
        file_path = os.path.join(self.tmp_path, 'file')
        with open(file_path, 'w') as fin:
            fin.write('')
        path = PathInfo(file_path)
        self.assertEqual(path.file_size, 0)
        with open(file_path, 'w') as fin:
            fin.write('0' * 1024)
        path = PathInfo(file_path)
        self.assertEqual(path.file_size, 1024)

    def test_directory_doesnt_have_file_size_attribute(self):
        dir_path = os.path.join(self.tmp_path, 'dir2')
        os.mkdir(dir_path)
        path = PathInfo(dir_path)
        self.assertEqual(path.file_size, None)
    
    def test_directory_doesnt_have_file_type_attribute(self):
        dir_path = os.path.join(self.tmp_path, 'dir3')
        os.mkdir(dir_path)
        path = PathInfo(dir_path)
        self.assertEqual(path.file_type, None)

    def test_contents_returns_right_info(self):
        dir_path = os.path.join(self.tmp_path, 'dir4')
        os.mkdir(dir_path)
        files = ['f1.txt', 'f2', 'f3.mpeg']
        directories = ['d1', 'd2']
        for file in files:
            path = os.path.join(dir_path, file)
            with open(path, 'w') as f:
                f.write('')
        for dir in directories:
            path = os.path.join(dir_path, dir)
            os.mkdir(path)
        path_info = PathInfo(dir_path)
        self.assertEqual(path_info.total_contents, len(files + directories))
        for info in path_info.contents:
            name = info.file_name
            self.assertIn(name, files + directories)

    def test_contents_attr_of_PathInfo_is_PathInfo(self):
        dir_path = os.path.join(self.tmp_path, 'dir5')
        os.mkdir(dir_path)
        files = ['f1', 'f2', 'f3']
        for file in files:
            path = os.path.join(dir_path, file)
            os.mkdir(path)
        path_info = PathInfo(dir_path)
        for content in path_info.contents:
            self.assertIsInstance(content, PathInfo)

    def test_directory_type_is_dir(self):
        path = os.path.join(self.tmp_path, 'test_directory_type_is_dir')
        os.mkdir(path)
        dir = PathInfo(path)
        self.assertEqual(dir.path_type, PathTypes.DIRECTORY.value)

    def test_file_type_is_file(self):
        file_path = os.path.join(self.tmp_path, 'test_file_type_is_file')
        with open(file_path, 'w') as fin:
            fin.write('')
        file = PathInfo(file_path)
        self.assertEqual(file.path_type, PathTypes.FILE.value)
        


    
       


        


