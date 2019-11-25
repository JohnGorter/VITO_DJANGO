from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import FileSerializer

class FilesUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        print(request.data)
        return Response("")

class FileUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)