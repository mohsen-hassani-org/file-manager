import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.files.exceptions import DirecotryAlreadyExistsException

from apps.files.utils import clean_path
from .path_info import PathInfo
from .serializers import PathInfoSerializer, DirectoryContentSerializer, NewDirectorySerializer
from .services import NewDirectoryService


class RootInfoAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        path_info = PathInfo(user.user_base_directory)
        serializer = DirectoryContentSerializer(path_info=path_info)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class PathInfoAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        current_path = clean_path(kwargs.get('path'))
        base_path = os.path.join(request.user.user_base_directory, current_path)
        path_info = PathInfo(base_path)
        serializer = DirectoryContentSerializer(path_info=path_info)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class NewDirectoryAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = NewDirectorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_directory = serializer.validated_data.get('directory_name')
        current_path = clean_path(kwargs.get('path'))
        base_path = os.path.join(request.user.user_base_directory, current_path)
        service = NewDirectoryService(path=base_path, new_directory_name=new_directory)
        try:
            path_info = service.execute()
        except DirecotryAlreadyExistsException:
            return Response({'error': 'This Directory already exists'}, status=status.HTTP_400_BAD_REQUEST)
        data = PathInfoSerializer(path_info=path_info).data
        return Response(data, status=status.HTTP_201_CREATED) 
    
