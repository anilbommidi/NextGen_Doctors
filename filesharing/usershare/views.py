from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.utils import json
from genericresponse import GenericResponse
from rest_framework.response import Response
from errormessage import Errormessage
from django.contrib.auth.hashers import check_password
from .models import OpsUser


class User_Register(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """ Here Ops User Can Register But Email id  Is Mandatory """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = UserSerializer(user).data
            response.Status = 200
            response.HasError = False
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=200)
        except Exception as e:
            response = GenericResponse("message", "result", "status", "has_error")
            response.Message = Errormessage(e)
            response.Result = False
            response.Status = 400
            response.HasError = True
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=400)


class Loginview(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Email = request.data.get('Email')
        password = request.data.get('Password')

        a = OpsUser.objects.get(Email=Email)
        if check_password(password, a.Password):
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = UserSerializer(a).data
            response.Status = 200
            response.HasError = False
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=200)
        else:
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Incorrect Password/UserName"
            response.Result = []
            response.Status = 400
            response.HasError = True
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=400)


class PasswordUpdate(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer

    # permission_classes = (IsAuthenticated,)

    def put(self, request, UserId):
        try:
            current_password = request.data.get('CurrentPassword')
            new_password = request.data.get('NewPassword')
            confirm_password = request.data.get('ConfirmPassword')
            user_query = OpsUser.objects.get(id=UserId)
            n = check_password(current_password, user_query.Password)
            if n and new_password == confirm_password:
                s = make_password(confirm_password)
                user_query.Password = s
                user = user_query.save()
                response = GenericResponse("Message", "Result", "Status", "HasError")
                response.Message = "Successful"
                response.Result = "Successfully Changed Your Password"
                response.Status = 200
                response.HasError = False
                jsonStr = json.dumps(response.__dict__)
                return Response(json.loads(jsonStr), status=200)
            else:
                response = GenericResponse("message", "result", "status", "has_error")
                response.Message = Errormessage("you entered password is wrong")
                response.Result = False
                response.Status = 400
                response.HasError = True
                jsonStr = json.dumps(response.__dict__)
                return Response(json.loads(jsonStr), status=400)

        except Exception as e:
            response = GenericResponse("message", "result", "status", "has_error")
            response.Message = Errormessage(e)
            response.Result = False
            response.Status = 400
            response.HasError = True
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=400)


class FileUploadView(generics.GenericAPIView):
    serializer_class = UploadedFileSerializer

    def post(self, request, *args, **kwargs):
        """Here User can upload files but Only pptx, docx, and xlsx files are allowed"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = UploadedFileSerializer(user).data
            response.Status = 200
            response.HasError = False
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=200)
        except Exception as e:
            response = GenericResponse("message", "result", "status", "has_error")
            response.Message = Errormessage(e)
            response.Result = False
            response.Status = 400
            response.HasError = True
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=400)
