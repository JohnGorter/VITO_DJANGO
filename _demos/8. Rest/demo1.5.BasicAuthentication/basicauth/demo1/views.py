from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Movie
from .serializers import MovieSerializer
from pytz import unicode


class IsAuth(BasePermission):
    def has_permission(self, request, view):
        return request.user != AnonymousUser


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ExampleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = "johngorter"
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


class MovieList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuth | ReadOnly]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        print('posting')
        return Response('')
        