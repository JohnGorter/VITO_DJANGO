from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def testview(Request):
    content = {
        'user': 'john',  # `django.contrib.auth.User` instance.
        'auth': 'none',  # None
    }
    return Response(content)
