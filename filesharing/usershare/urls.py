
from django.urls import path
from .views import *

urlpatterns = [
    path('User_Register/',User_Register.as_view()),
    path('User_Login/',Loginview.as_view()),
    path('Password_Change/<int:UserId>',PasswordUpdate.as_view()),
    path('File_Upload/',FileUploadView.as_view()),
]
