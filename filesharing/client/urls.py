from django.urls import path
from .views import *

urlpatterns = [
    path('Client_Register/',Client_Register.as_view()),
    path('Client_Login/',Loginview.as_view()),
    path('Password_Change/<int:UserId>',PasswordUpdate.as_view()),
    path('EmailVerification/', EmailView.as_view(), name='EmailView'),
    path('EmailOTPVerification/', EmailVerificationView.as_view(), name='EmailVerificationView'),
    path('Download/',GetFiles.as_view()),

]
