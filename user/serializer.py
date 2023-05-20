from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    uid = serializers.CharField()
    token = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()