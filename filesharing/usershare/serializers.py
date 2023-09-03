import base64

from rest_framework import serializers
from .models import OpsUser, UploadedFile
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsUser
        fields = ['Firstname', 'Lastname', 'Email', 'Password']

    def create(self, validated_data):
        user = OpsUser.objects.create(Firstname=validated_data['Firstname'], Lastname=validated_data['Lastname'],
                                      Email=validated_data['Email'],
                                      Password=(make_password(validated_data['Password'])))

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsUser
        fields = ['Email', 'Password']


class PasswordChangeSerializer(serializers.Serializer):
    UserId = serializers.IntegerField()
    CurrentPassword = serializers.CharField()
    NewPassword = serializers.CharField()
    ConfirmPassword = serializers.CharField()


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['user', 'file', 'file_content']

    def create(self, validated_data):
        file = validated_data['file']

        file_extension = file.name.split('.')[-1].lower()
        valid_extensions = ['pptx', 'docx', 'xlsx']

        if file_extension not in valid_extensions:
            raise serializers.ValidationError("Invalid file type. Only pptx docx and xlsx files are allowed.")

        encoded_file = base64.b64encode(file.read())
        uploaded_file = UploadedFile.objects.create(
            user=validated_data['user'],
            file=ContentFile(file.read(), name=file.name),
            file_content=encoded_file,
        )

        return uploaded_file
