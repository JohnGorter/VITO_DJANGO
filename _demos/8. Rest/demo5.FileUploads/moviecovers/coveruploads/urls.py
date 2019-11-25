from django.urls import path
from .views import *

urlpatterns = [
    path('single', FileUploadView.as_view()),
    path('multiple', FilesUploadView.as_view())
   
]