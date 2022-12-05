from rest_framework import serializers
from accounts.models import MyUser


class UserSerializer(serializers.Serializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'id')