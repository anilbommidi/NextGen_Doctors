from usershare.models import *
from rest_framework import serializers
from .models import Client,EmailModel
from django.contrib.auth.hashers import make_password



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['Firstname', 'Lastname', 'Email', 'Password']

    def create(self, validated_data):
        user = Client.objects.create(Firstname=validated_data['Firstname'], Lastname=validated_data['Lastname'],
                                      Email=validated_data['Email'],
                                      Password=(make_password(validated_data['Password'])))

        user.save()
        return user


class ClientLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['Email', 'Password']


class ClientPasswordChangeSerializer(serializers.Serializer):
    UserId = serializers.IntegerField()
    CurrentPassword = serializers.CharField()
    NewPassword = serializers.CharField()
    ConfirmPassword = serializers.CharField()


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = ['Email']


class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = ["Email", "Otp"]


class GetUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

