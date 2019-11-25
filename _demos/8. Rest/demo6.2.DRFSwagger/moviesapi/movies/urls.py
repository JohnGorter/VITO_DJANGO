from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MovieView.as_view())
]


