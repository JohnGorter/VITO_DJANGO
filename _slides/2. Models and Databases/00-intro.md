# Models and Databases

---
### Models (1)

A model is the single, definitive source of data about your data
- It contains the essential fields and behaviors of the data

Each model maps to a single database table

---
### Models (2)
The basics

- Each model is a Python class that subclasses django.db.models.Model
- Each attribute of the model represents a database field

Django gives you an automatically-generated database-access API

---
### Quick example
This example model defines a Person, which has a first_name and last_name

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

- Each field is specified as a class attribute
- Each attribute maps to a database column

---
### Quick Example (2)
This would create a database table like

```
CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

Note
- the name of the table, myapp_person, is automatically derived 
  - but can be overridden
- an id field is added automatically
  - but can be overridden

Django uses SQL tailored to the database backend specified in your settings file

---
### Using models

To use the models:
- edit your settings file 
- example
```
INSTALLED_APPS = [
    #...
    'myapp',
    #...
]
```
- run manage.py migrate
- optionally make migrations with manage.py makemigrations

---
### Fields

The most important part of a model and the only required part of a model 

```
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

---
### Field types
Each field is an instance of a Field class
Django uses the field class types to determine

- the column type (e.g. INTEGER, VARCHAR, TEXT)
- the default HTML widget for a form field (e.g. <input type="text">, <select></select>)
- the validation requirements (used in Django’s admin and in automatically-generated forms)

Django ships with dozens of built-in field types
- You can easily write your own fields too

---
### Field options (1)
Each field takes a certain set of field-specific arguments

Example: CharField require a max_length argument which specifies the size of the VARCHAR database

There’s also a set of common arguments available to all field types. 
- all are optional

---
### Field options (2)
The most often-used ones
- null: if True, Django will store empty values as NULL in the database. Default is False.
- blank: if True, the field is allowed to be blank. Default is False.
- choices: sequence of 2-tuples to use as choices for this field

> Null is purely database-related, whereas blank is validation-related
 
> If a field has blank=True, form validation will allow entry of an empty value

> If a field has blank=False, the field will be required

---
### Choices
A sequence of 2-tuples to use as choices for this field. 

The default form widget will be a select box instead of the standard text field 

A choices list looks like this
```
YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]
```

The first element in each tuple is the value, the second element is displayed by the field’s form widget

---
### Choices example 
Here is an example of a choices field
```
# Create your models here.
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Choices

---
### More field options (1)

- Default: default value for the field
  - can be a value or a callable object
  - if callable it will be called every time a new object is created
- Help_text: extra “help” text to be displayed with the form widget
- Primary_key: if True, this field is the primary key for the model
- Unique: if True, this field must be unique throughout the table

If you don’t specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key

The primary key field is read-only

---
### More field options (2)
If you change the value of the primary key on an existing object and save it, a new object will be created. 

For example:
```
from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
```

```
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
<QuerySet ['Apple', 'Pear']>
```

---
### Verbose field names

Each field type takes an optional first positional argument 
- except for ForeignKey
- ManyToManyField 
- OneToOneField

If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces

In this example, the verbose name is "person's first name":
```
first_name = models.CharField("person's first name", max_length=30)
```
In this example, the verbose name is "first name":
```
first_name = models.CharField(max_length=30)
```

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Models



