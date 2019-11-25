from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MovieList.as_view())
]
