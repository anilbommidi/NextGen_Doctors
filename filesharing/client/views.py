from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.utils import json
from genericresponse import GenericResponse
from rest_framework.response import Response
from errormessage import Errormessage
from django.contrib.auth.hashers import check_password
from .models import Client,EmailModel
from django.core.mail import send_mail
from django.http import JsonResponse
import random
import math
from django.conf import settings

from usershare.models import UploadedFile


class Client_Register(generics.GenericAPIView):
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        """ Here Ops User Can Register But Email id  Is Mandatory """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = ClientSerializer(user).data
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
    serializer_class = ClientLoginSerializer

    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Email = request.data.get('Email')
        password = request.data.get('Password')

        a = Client.objects.get(Email=Email)
        if check_password(password, a.Password):
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = ClientSerializer(a).data
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
    serializer_class = ClientPasswordChangeSerializer

    # permission_classes = (IsAuthenticated,)

    def put(self, request, UserId):
        try:
            current_password = request.data.get('CurrentPassword')
            new_password = request.data.get('NewPassword')
            confirm_password = request.data.get('ConfirmPassword')
            user_query = Client.objects.get(id=UserId)
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


def GenerateOtp():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp


class EmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Here We Generating OTP"""

        try:
            Email = request.data.get('Email')
            Otp = GenerateOtp()
            EmailModel.objects.create(Email=Email, Otp=Otp)
            message = Otp
            subject = 'Subject of the email'
            sender = settings.FROM_EMAIL
            recipient = [Email]
            send_mail(subject, message, sender, recipient)
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = EmailSerializer.data
            response.Status = 200
            response.HasError = False
            return JsonResponse({'Email': Email, 'Otp': Otp}, status=200)
        except Exception as e:
            response = GenericResponse("message", "result", "status", "has_error")
            response.Message = Errormessage(e)
            response.Result = False
            response.Status = 400
            response.HasError = True
            jsonStr = json.dumps(response.__dict__)
            return Response(json.loads(jsonStr), status=400)


# def delete_otp(id):
#
#     import pymongo
#
#     myclient = pymongo.MongoClient("localhost:27017/")
#     mydb = myclient["db"]
#     mycol = mydb["Table"]
#     mycol.delete_one({'id': id})


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Here We validating OTP"""

        try:

            Email = request.data.get('Email')
            Otp = request.data.get('Otp')
            number = EmailModel.objects.filter(Email=Email)
            num_values = number.values()
            new_list = []
            for each in num_values:
                new_list.append(dict(each))
            get_otp = new_list[-1]['Otp']
            id = new_list[-1]['id']
            print(get_otp)
            if Otp == get_otp:
                # delete_otp(id)
                response = GenericResponse("Message", "Result", "Status", "HasError")
                response.Message = "Successful"
                response.Result = "Email Verification is Successful"
                response.Status = 200
                response.HasError = False
                jsonStr = json.dumps(response.__dict__)
                return Response(json.loads(jsonStr), status=200)
            else:
                response = GenericResponse("Message", "Result", "Status", "HasError")
                response.Message = "Please enter valid Otp"
                response.Result = "Email Verification is UnSuccessful"
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


class GetFiles(generics.GenericAPIView):
    serializer_class = GetUploadedFileSerializer
    queryset = UploadedFile.objects.all()

    def get(self, request, *args, **kwargs):

        try:
            a = UploadedFile.objects.all()
            print(a)
            response = GenericResponse("Message", "Result", "Status", "HasError")
            response.Message = "Successful"
            response.Result = GetUploadedFileSerializer(a).data
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
