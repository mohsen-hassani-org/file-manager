from rest_framework import generics, views, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer
from .models import User
from .services import RegisterUserService


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        service = RegisterUserService(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user = service.execute()
        serializer.instance = user
