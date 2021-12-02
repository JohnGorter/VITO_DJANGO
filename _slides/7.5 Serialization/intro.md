# Serializing Django objects

“translating” Django models into other formats

---
### Serializing data
At the highest level, you can serialize data like this:
```
from django.core import serializers
data = serializers.serialize("xml", SomeModel.objects.all())
```

---
### Serializing data
You can also use a serializer object directly:
```
XMLSerializer = serializers.get_serializer("xml")
xml_serializer = XMLSerializer()
xml_serializer.serialize(queryset)
data = xml_serializer.getvalue()
```

This is useful if you want to serialize data directly to a file-like object
- which includes an HttpResponse)
```
with open("file.xml", "w") as out:
    xml_serializer.serialize(SomeModel.objects.all(), stream=out)
```

---
### Serializing data
Calling get_serializer() with an unknown format will raise a django.core.serializers.SerializerDoesNotExist exception.

---
### Subset of fields
If you only want a subset of fields to be serialized
```
from django.core import serializers
data = serializers.serialize('xml', SomeModel.objects.all(), fields=('name','size'))
```

In this example, only the name and size attributes of each model will be serialized


---
### Inherited models
If you have a model that is defined using an abstract base class, you don’t have to do anything special to serialize that model. Call the serializer on the object (or objects) that you want to serialize, and the output will be a complete representation of the serialized object

---
### Inherited models
However, if you have a model that uses *multi-table* inheritance, you also need to serialize all of the base classes for the model. This is because only the fields that are locally defined on the model will be serialized. For example, consider the following models:

```
class Place(models.Model):
    name = models.CharField(max_length=50)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
```
If you only serialize the Restaurant model:
```
data = serializers.serialize('xml', Restaurant.objects.all())
```
the fields on the serialized output will only contain the serves_hot_dogs attribute
- the name attribute of the base class will be ignored


---
### Inherited models
In order to fully serialize your Restaurant instances, you will need to serialize the Place models as well:
```
all_objects = [*Restaurant.objects.all(), *Place.objects.all()]
data = serializers.serialize('xml', all_objects)
```

---
### Deserializing data
Deserializing data is very similar to serializing it:
```
for obj in serializers.deserialize("xml", data):
    do_something_with(obj)
```

- returns an iterator.

---
### Deserializing data
The objects returned by the deserialize iterator aren’t regular Django objects
- they are special DeserializedObject instances that wrap a created – but unsaved – object and any associated relationship data

Calling DeserializedObject.save() saves the object to the database

Note
> If the pk attribute in the serialized data doesn’t exist or is null, a new instance will be saved to the database

---
### Deserializing data
Usually, working with these DeserializedObject instances looks something like

```
for deserialized_object in serializers.deserialize("xml", data):
    if object_should_be_saved(deserialized_object):
        deserialized_object.save()
```


---
### Serialization formats
Django supports a number of serialization formats
- some of which require you to install third-party Python modules:

- xml	Serializes to and from a simple XML dialect
- json	Serializes to and from JSOM
- jsonl	Serializes to and from JSONL
- yaml	Serializes to YAML (YAML Ain’t a Markup Language)
    - This serializer is only available if PyYAML is installed.


---
### XML
The basic XML serialization format looks like this:
```
<?xml version="1.0" encoding="utf-8"?>
<django-objects version="1.0">
    <object pk="123" model="sessions.session">
        <field type="DateTimeField" name="expire_date">2013-01-16T08:16:59.844560+00:00</field>
        <!-- ... -->
    </object>
</django-objects>
```

---
### XML

Foreign keys and other relational fields are treated a little bit differently:
```
<object pk="27" model="auth.permission">
    <!-- ... -->
    <field to="contenttypes.contenttype" name="content_type" rel="ManyToOneRel">9</field>
    <!-- ... -->
</object>
```

In this example we specify that the auth.Permission object with the PK 27 has a foreign key to the contenttypes.ContentType instance with the PK 9.

---
### XML
ManyToMany-relations are exported for the model that binds them. For instance, the auth.User model has such a relation to the auth.Permission model:

```
<object pk="1" model="auth.user">
    <!-- ... -->
    <field to="auth.permission" name="user_permissions" rel="ManyToManyRel">
        <object pk="46"></object>
        <object pk="47"></object>
    </field>
</object>
```

This example links the given user with the permission models with PKs 46 and 47.

---
### Control characters

If the content to be serialized contains control characters that are not accepted in the XML 1.0 standard, the serialization will fail with a ValueError exception

---
### JSON
When staying with the same example data as before it would be serialized as JSON in the following way

```
[
    {
        "pk": "4b678b301dfd8a4e0dad910de3ae245b",
        "model": "sessions.session",
        "fields": {
            "expire_date": "2013-01-16T08:16:59.844Z",
            ...
        }
    }
]
```

---
### JSON
Be aware that not all Django output can be passed unmodified to json. For example, if you have some custom type in an object to be serialized, you’ll have to write a custom json encoder for it. Something like this will work

```
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)
```
You can then pass cls=LazyEncoder to the serializers.serialize() function:
```
from django.core.serializers import serialize

serialize('json', SomeModel.objects.all(), cls=LazyEncoder)
```

---
### DjangoJSONEncoder
The JSON serializer uses DjangoJSONEncoder for encoding
- a subclass of JSONEncoder

It handles these additional types
- datetime
A string of the form YYYY-MM-DDTHH:mm:ss.sssZ or YYYY-MM-DDTHH:mm:ss.sss+HH:MM as defined in ECMA-262.
- date
A string of the form YYYY-MM-DD as defined in ECMA-262.
- time
A string of the form HH:MM:ss.sss as defined in ECMA-262.
- timedelta
A string representing a duration as defined in ISO-8601. For example, timedelta(days=1, hours=2, seconds=3.4) is represented as 'P1DT02H00M03.400000S'.
Decimal, Promise (django.utils.functional.lazy() objects), UUID
A string representation of the object.

---
### JSONL
JSONL stands for JSON Lines. With this format, objects are separated by new lines, and each line contains a valid JSON object. JSONL serialized data looks like this
```
{"pk": "4b678b301dfd8a4e0dad910de3ae245b", "model": "sessions.session", "fields": {...}}
{"pk": "88bea72c02274f3c9bf1cb2bb8cee4fc", "model": "sessions.session", "fields": {...}}
{"pk": "9cf0e26691b64147a67e2a9f06ad7a53", "model": "sessions.session", "fields": {...}}
```

JSONL can be useful for populating large databases, since the data can be processed line by line, rather than being loaded into memory all at once

---
### YAML
YAML serialization looks quite similar to JSON. The object list is serialized as a sequence mappings with the keys “pk”, “model” and “fields”

Each field is again a mapping with the key being name of the field and the value the value:
```
-   fields: {expire_date: !!timestamp '2013-01-16 08:16:59.844560+00:00'}
    model: sessions.session
    pk: 4b678b301dfd8a4e0dad910de3ae245b
```

Referential fields are again represented by the PK or sequence of PKs.


---
### Natural keys
A natural key is a tuple of values that can be used to uniquely identify an object instance without using the primary key value

---
### Deserialization of natural keys
Consider the following two models:
```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    birthdate = models.DateField()

    class Meta:
        unique_together = [['first_name', 'last_name']]

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
```

---
### Deserialization of natural keys
Ordinarily, serialized data for Book would use an integer to refer to the author. For example, in JSON, a Book might be serialized as:

```
...
{
    "pk": 1,
    "model": "store.book",
    "fields": {
        "name": "Mostly Harmless",
        "author": 42
    }
}
...
```

This isn’t a particularly natural way to refer to an author. It requires that you know the primary key value for the author
- it also requires that this primary key value is stable and predictable

---
### Deserialization of natural keys
If we add natural key handling to Person, the fixture becomes much more humane

To add natural key handling, you define a default Manager for Person with a get_by_natural_key() method

```
from django.db import models

class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = PersonManager()

    class Meta:
        unique_together = [['first_name', 'last_name']]
```


---
### Deserialization of natural keys
Now books can use that natural key to refer to Person objects:
```
...
{
    "pk": 1,
    "model": "store.book",
    "fields": {
        "name": "Mostly Harmless",
        "author": ["Douglas", "Adams"]
    }
}
...
```

Deserialization of objects with no primary key will always check whether the model’s manager has a get_by_natural_key() method and if so, use it to populate the deserialized object’s primary key

---
### Serialization of natural keys
So how do you get Django to emit a natural key when serializing an object? Firstly, you need to add another method 

– this time to the model itself:
```
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = PersonManager()

    class Meta:
        unique_together = [['first_name', 'last_name']]

    def natural_key(self):
        return (self.first_name, self.last_name)
```

That method should always return a natural key tuple – in this example, (first name, last name)

---
### Serialization of natural keys
When you call serializers.serialize(), you provide use_natural_foreign_keys=True or use_natural_primary_keys=True arguments:
```
>>> serializers.serialize('json', [book1, book2], indent=2,
...      use_natural_foreign_keys=True, use_natural_primary_keys=True)
```

When use_natural_foreign_keys=True is specified, Django will 
- use the natural_key() method to serialize any foreign key reference to objects of the type that defines the method
- not provide the primary key in the serialized data of this object since it can be calculated during deserialization:

```
...
{
    "model": "store.person",
    "fields": {
        "first_name": "Douglas",
        "last_name": "Adams",
        "birth_date": "1952-03-11",
    }
}
...
```

---
### Natural keys and forward references
Sometimes when you use natural foreign keys you’ll need to deserialize data where an object has a foreign key referencing another object that hasn’t yet been deserialized. This is called a “forward reference”.

For instance, suppose you have the following objects in your fixture:
```
...
{
    "model": "store.book",
    "fields": {
        "name": "Mostly Harmless",
        "author": ["Douglas", "Adams"]
    }
},
...
{
    "model": "store.person",
    "fields": {
        "first_name": "Douglas",
        "last_name": "Adams"
    }
},
...
```
In order to handle this situation, you need to pass handle_forward_references=True to serializers.deserialize()

This will set the deferred_fields attribute on the DeserializedObject instances

---
### Natural keys and forward references
You’ll need to keep track of DeserializedObject instances where this attribute isn’t None and later call save_deferred_fields() on them

Typical usage looks like this:
```
objs_with_deferred_fields = []

for obj in serializers.deserialize('xml', data, handle_forward_references=True):
    obj.save()
    if obj.deferred_fields is not None:
        objs_with_deferred_fields.append(obj)

for obj in objs_with_deferred_fields:
    obj.save_deferred_fields()
```
For this to work, the ForeignKey on the referencing model must have null=True

---
### Dependencies during serialization
It’s often possible to avoid explicitly having to handle forward references by taking care with the ordering of objects within a fixture

To help with this, calls to dumpdata that use the dumpdata --natural-foreign option will serialize any model with a natural_key() method before serializing standard primary key objects

However, this may not always be enough. If your natural key refers to another object (by using a foreign key or natural key to another object as part of a natural key), then you need to be able to ensure that the objects on which a natural key depends occur in the serialized data before the natural key requires them.

To control this ordering, you can define dependencies on your natural_key() methods. You do this by setting a dependencies attribute on the natural_key() method itself.

---
### Dependencies during serialization
For example, let’s add a natural key to the Book model from the example above:
```
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.name,) + self.author.natural_key()
```

The natural key for a Book is a combination of its name and its author. This means that Person must be serialized before Book. To define this dependency, we add one extra line:
```
def natural_key(self):
    return (self.name,) + self.author.natural_key()
natural_key.dependencies = ['example_app.person']
```
This definition ensures that all Person objects are serialized before any Book objects. In turn, any object referencing Book will be serialized after both Person and Book have been serialized

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Serializing data


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Serializing data