# REST

---
### REST

REpresentational State Transfer
- Roy Fielding
- HTTP verbs and entities

REST in DJANGO
- DRF 

---
### DJANGO Rest Framework

> Django REST framework is a powerful and flexible toolkit for building Web APIs.

DJANGO supports REST api similar to ModelForms 

Topics include
- Serializers
- Requests and Responses
- Function and Class based views
- Authentication and Persmission
- Viewsets and Routers

---
### DJANGO Rest Framework

Installation
```
pip install djangorestframework
```

Configuration
settings.py
```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'yourapp',
]
```

---
### Serializers

Serializers take an instance of a model and 
convert them to Pyhton native datatypes 

From there this can be seralized to JSON or XML

Just like forms, there are two types
- Serializer
- ModelSerializer

---
### Serializers (2)

An example of a serializer
```
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=20)
    description = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
```

Note that serializer.save() calls create() or update() automatically..

---
### Conversion to JSON

To convert serializers data to JSON you need a JSONRenderer
```
from rest_framework.renderers import JSONRenderer

...
content = JSONRenderer().render(serializer.data)
print(content)
```

---
### Conversion from JSON

to convert a JSON string to an object instance, you need a JSONParser
```
from rest_framework.parsers import JSONParser

import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = MovieSerializer(data=data)
serializer.is_valid()
serializer.validated_data

# OrderedDict([('title', ''), ('description', 'test')])
serializer.save()
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using a serializer

---
### ModelSerializer

- provides a shortcut that lets you automatically create a Serializer class with fields that correspond to the Model fields

- is the same as a regular Serializer class, except that
    - it will automatically generate a set of fields for you, based on the model
    - it will automatically generate validators for the serializer, such as unique_together validators
    - it includes simple default implementations of .create() and .update()

---
### ModelSerializer

example of a ModelSerializer
```
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description']
```



---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using a ModelSerializer

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
ModelSerializers

