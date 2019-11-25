# Parsers

---
### Parsers
Parser classes allow you to accept requests with various media types
- support for defining your own custom parsers

---
### Parser determined
The set of valid parsers for a view is always defined as a list of classes

When request.data is accessed DRF examines the Content-Type header

Note: When developing client applications remember to set the Content-Type header when sending data.

If you don't set the content type, most clients will default to using 'application/x-www-form-urlencoded', which may not be what you wanted.

---
### Parse example
As an example, if you are sending json encoded data using jQuery with the .ajax() method, you should make sure to include the contentType: 'application/json' setting.

---
### Setting the parsers
The default set of parsers may be set globally, using the DEFAULT_PARSER_CLASSES setting. 

Example
```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

---
### Setting the parsers
You can also set the parsers used for an individual view, or viewset, using the APIView class-based views.

```
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        return Response({'received data': request.data})
```

Or, if you're using the @api_view decorator with function based views

```
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes([JSONParser])
def example_view(request, format=None):
    """
    A view that can accept POST requests with JSON content.
    """
    return Response({'received data': request.data})
```

---
### Parsers available
This is the list of parsers DRF supplies:
- JSONParser
- FormParser
- MultiPartParser
- FileUploadParser

---
### JSONParser
Parses JSON request content
- .media_type: application/json

---
### FormParser
Parses HTML form content
- request.data is populated with a QueryDict of data.
- .media_type: application/x-www-form-urlencoded

---
### MultiPartParser
Parses multipart HTML form content
- supports file uploads
- request.data is populated with a QueryDict
- .media_type: multipart/form-data

You will typically want to use both FormParser and MultiPartParser together in order to fully support HTML form data.

---
### FileUploadParser
Parses raw file upload content
- request.data property is a dictionary with key 'file' containing the uploaded file.
- .media_type: */*

If the view used with FileUploadParser is called with a filename URL keyword argument, then that argument will be used as the filename.

If it is called without a filename URL keyword argument, then the client must set the filename in the Content-Disposition HTTP header.

example 
```
Content-Disposition: attachment; filename=upload.jpg.
```


---
### FileUploadParser vs MultiPartParser

The FileUploadParser is for usage with native clients that can upload the file as a raw data request. The MultiPartParser is for web-based uploads, or for native clients with multipart upload support

Since this parser's media_type matches any content type, FileUploadParser should generally be the only parser set on an API view

---
### FileUploadParser Example

Basic usage example:
```
# views.py
class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

# urls.py
urlpatterns = [
    # ...
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
```

---
### Custom parsers
To implement a custom parser
- override BaseParser
- set the .media_type property
- implement the .parse(self, stream, media_type, parser_context) method

The method should return the data that will be used to populate the request.data property

---
### Custom parsers, parse method
The arguments passed to .parse() are:
- stream
A stream-like object representing the body of the request.
- media_type
Optional. If provided, this is the media type of the incoming request content.
- parser_context
Optional. If supplied, this argument will be a dictionary containing any additional context that may be required to parse the request content. By default this will include the following keys: view, request, args, kwargs.

---
### Custom parsers example 

Example plaintext parser
```
class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
```

---
### Third party packages
The following third party packages are also available.
- YAML -> YAML parsing and rendering support
- XML -> simple informal XML format parser
- MessagePack -> a fast, efficient binary serialization format
- CamelCase JSON -> allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names

---
### YAML
REST framework YAML provides YAML parsing and rendering support. It was previously included directly in the REST framework package, and is now instead supported as a third-party package.

- Install using pip
```
$ pip install djangorestframework-yaml
```
- config through settings.py
```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_yaml.parsers.YAMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_yaml.renderers.YAMLRenderer',
    ],
}
```

---
### XML
REST Framework XML provides a simple informal XML format

- Install using pip.
```
$ pip install djangorestframework-xml
```

- config through settings.py
```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_xml.parsers.XMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_xml.renderers.XMLRenderer',
    ],
}
```

---
### MessagePack
MessagePack is a fast, efficient binary serialization format. Juan Riaza maintains the djangorestframework-msgpack package which provides MessagePack renderer and parser support for REST framework.

---
### CamelCase JSON
djangorestframework-camel-case provides camel case JSON renderers and parsers for REST framework. This allows serializers to use Python-style underscored field names, but be exposed in the API as Javascript-style camel case field names. It is maintained by Vitaly Babiy.

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
File Uploads in DRF

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Supplying Multiple Files in File Upload






