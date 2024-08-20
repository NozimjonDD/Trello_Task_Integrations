from rest_framework import generics, permissions

from apps.users import models

from . import serializers


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
