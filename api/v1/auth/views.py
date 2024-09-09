from rest_framework import generics, permissions

from apps.users import models
from . import serializers


class UserRegisterAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = serializers.UserRegisterSerializer
    queryset = models.User.objects.all()


class UserRegisterConfirmAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = serializers.UserRegisterConfirmSerializer
    queryset = models.User.objects.all()


# class ResetPasswordAPIView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = serializers.UserRegisterSerializer
#     queryset = models.User.objects.all()


class ChangePasswordAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer
    queryset = models.User.objects.all()


class DeleteAccountAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DeleteAccountSerializer
    queryset = models.User.objects.all()


class DeleteAccountConfirmAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DeleteAccountConfirmSerializer
    queryset = models.User.objects.all()
