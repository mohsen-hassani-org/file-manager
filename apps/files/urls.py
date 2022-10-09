"""
    /api/v1/files/                         => my all files in root
    /api/v1/files/<path>/                  => details of a path (including subfiles in case of directory) 
    /api/v1/files/info/<path>/             => download a file or raise in case of directory
    /api/v1/files/download/<path>/         => download a file or raise in case of directory
    /api/v1/files/delete/<path>/           => delete a file or raise in case of directory
    /api/v1/files/new-directory/<path>/    => new directory in this path or raise error in case of folder
    /api/v1/files/upload/<path>/           => upload new file here
    /api/v1/files/move/<path>/           => upload new file here
"""
from django.urls import path
from .views import PathInfoAPI, RootInfoAPI, NewDirectoryAPI


app_name = 'files'


urlpatterns = [
    path('', RootInfoAPI.as_view(), name='root_files'),
    path('new-directory/<path:path>/', NewDirectoryAPI.as_view(), name='new_directory'),
    path('<path:path>/', PathInfoAPI.as_view(), name='path_files'),
]