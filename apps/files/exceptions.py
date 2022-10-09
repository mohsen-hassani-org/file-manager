from rest_framework.exceptions import APIException


class DirectoryDoesntHaveSizeAttribute(APIException):
    pass

class DirectoryDoesntHaveTypeAttribute(APIException):
    pass

class FileDoesntHaveContentAttribute(APIException):
    pass

class DirecotryAlreadyExistsException(APIException):
    pass

