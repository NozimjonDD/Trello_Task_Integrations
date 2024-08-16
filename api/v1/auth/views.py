from rest_framework import generics, permissions

from users import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegisterSerializer
    queryset = models.User.objects.all()
