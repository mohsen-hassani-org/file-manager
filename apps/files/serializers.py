from rest_framework import serializers
from .mixins import SerializerPathInfoMixin


class BasePathInfoSerializer(SerializerPathInfoMixin, serializers.Serializer):
    full_path = serializers.CharField(read_only=True)
    path_type = serializers.CharField(read_only=True)
    file_name = serializers.CharField(read_only=True)
    file_extension = serializers.CharField(read_only=True)
    file_size = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    last_modified = serializers.CharField(read_only=True)

    def get_attribute(self, instance):
        return super().get_attribute(instance)

    def to_representation(self, instance):
        return super().to_representation(instance)

class PathInfoSerializer(BasePathInfoSerializer):
    pass

class DirectoryContentSerializer(BasePathInfoSerializer):
    contents = BasePathInfoSerializer(read_only=True, many=True)

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    

class NewDirectorySerializer(serializers.Serializer):
    directory_name = serializers.CharField(max_length=255)
