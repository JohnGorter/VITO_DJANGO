# Advanced models


---
### Manager

The most important attribute of a model is the Manager
- it’s the interface through which database query operations are provided  
- used to retrieve the instances from the database. 

If no custom Manager is defined, the default name is 'objects'

Managers are only accessible via model classes, not the model instances

---
### Other Model methods
Define custom methods on a model to add custom “row-level” functionality to your objects

- Manager methods are intended to do “table-wide” things model methods should act on a particular model instance

This is a valuable technique for keeping business logic in one place –> the model

---
### Model methods (2)
This model has a few custom methods
```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
```

The last method in this example is a property

---
### Model Methods (3)
Override model method candidates

- \_\_str\_\_() 
    - a Python “magic method” that returns a string representation of any object

- get_absolute_url()
    - the URL for an object Django uses this in its admin interface
    - any object that has a URL that uniquely identifies it should define this method

---
### Model methods (4)

There’s another set of model methods that encapsulate a bunch of database behavior that you’ll want to customize

In particular you’ll often want to change the way save() and delete() work

Example override of save method
```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        do_something_else()
```

---
### Model methods (5)

Or you can also prevent saving

```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return # Yoko shall never have her own blog!
        else:
            super().save(*args, **kwargs)  # 
```

---
### Superclass call

It’s important to remember to call the superclass method 
    – to ensure that the object still gets saved into the database. 
    - if you forget to call the superclass method, the default behavior won’t happen and the database won’t get touched.

It’s also important that you pass through the arguments that can be passed to the model method 
    - Django will, from time to time, extend the capabilities of built-in model methods, adding new arguments
    
---
### Executing custom SQL

Another common pattern is writing custom SQL statements in model methods and module-level methods

More info later...

---
### Model inheritance
There are three styles of inheritance that are possible in Django.

- Abstract base classes
Often, you will just want to use the parent class to hold information that you don’t want to have to type out for each child model. This class isn’t going to ever be used in isolation

- Multi-table inheritance
If you’re subclassing an existing model (perhaps something from another application entirely) and want each model to have its own database table

- Proxy models
If you only want to modify the Python-level behavior of a model, without changing the models fields in any way


---
### Abstract base classes

When you want common information into a number of other models

Write your base class and put abstract=True in the Meta class
- this model will not be used to create any database table
- when it is used as a base class for other models, its fields will be added to those of the child class

Example
```
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

> Fields inherited from abstract base classes can be overridden or removed with None

---
### Meta inheritance
When an abstract base class is created, Django makes any Meta inner class you declared in the base class available as an attribute

If a child class does not declare its own Meta class, it will inherit the parent’s Meta

If the child wants to extend the parent’s Meta class, it can subclass it. 

Example
```
from django.db import models

class CommonInfo(models.Model):
    # ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    # ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```

---
### Multi-table inheritance
Each model in the hierarchy is a model all by itself

Each model corresponds to its own database table and can be queried and created individually 

The inheritance relationship introduces links between the child model and each of its parents (via an automatically-created OneToOneField). 

Example:
```
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

```

---
### Multi-table inheritance (2)
All of the fields of Place will also be available in Restaurant, although the data will reside in a different database table

```
>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")
```

If Place is also a Restaurant, you can get from the Place object to the Restaurant object by using the lowercase version of the model name
```
>>> p = Place.objects.get(id=12)
>>> p.restaurant
<Restaurant: ...>
```

However, if p in the above example was not a Restaurant referring to p.restaurant would raise a Restaurant.DoesNotExist exception

---
### Multi-table inheritance (3)
The automatically-created OneToOneField on Restaurant that links it to Place looks like this:

```
place_ptr = models.OneToOneField(
    Place, on_delete=models.CASCADE,
    parent_link=True,
)
```

You can override that field by declaring your own OneToOneField with parent_link=True on Restaurant

---
### Meta and multi-table inheritance (1)
In this situation, it doesn’t make sense for a child class to inherit from its parent’s Meta class

All the Meta options have already been applied to the parent class

A child model does not have access to its parent’s Meta class

There are a few limited cases where the child inherits behavior from the parent
- if the child does not specify 
    - an ordering attribute
    - a get_latest_by attribute
it will inherit these from its parent

---
### Meta and multi-table inheritance (2)

If the parent has an ordering and you don’t want the child to have any natural ordering, you can explicitly disable it

```
class ChildModel(ParentModel):
    # ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []
```

---
### Proxy models
Sometimes, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method

You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the original (non-proxied) model

The difference is that you can change things like the default model ordering or the default manager in the proxy, without having to alter the original

Proxy models are declared like normal models, tell Django that it’s a proxy model by setting the proxy attribute of the Meta class to True

---
### Proxy models (1)
For example, suppose you want to add a method to the Person model. You can do it like this
```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```


---
### Proxy models (2)

The MyPerson class operates on the same database table as its parent Person class. In particular, any new instances of Person will also be accessible through MyPerson, and vice-versa:

```
>>> p = Person.objects.create(first_name="foobar")
>>> MyPerson.objects.get(first_name="foobar")
<MyPerson: foobar>
```

---
### Proxy models (3)
You could also use a proxy model to define a different default ordering on a model 

You might not always want to order the Person model, but regularly order by the last_name attribute when you use the proxy

```
class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True
```

Now normal Person queries will be unordered and OrderedPerson queries will be ordered by last_name

---
### Base class restrictions
- A proxy model must inherit from exactly one non-abstract model class
- A proxy model can inherit from any number of abstract model classes, providing they do not define any model fields
- A proxy model may also inherit from any number of proxy models that share a common non-abstract parent class



---
### Multiple inheritance (1)
It’s possible for a Django model to inherit from multiple parent models

The first base class that a particular name (e.g. Meta) appears in will be the one that is used 
- this means that if multiple parents contain a Meta class, only the first one is going to be used, and all others will be ignored

Generally, you won’t need to inherit from multiple parents

The main use-case where this is useful is for “mix-in” classes: adding a particular extra field or method to every class that inherits the mix-in

---
### Multiple inheritance (2)
Note that inheriting from multiple models that have a common id primary key field will raise an error. To properly use multiple inheritance, you can use an explicit AutoField in the base models

```
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    ...

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ...

class BookReview(Book, Article):
    pass
```

---
### Field name “hiding” is not permitted
In normal Python class inheritance, it is permissible for a child class to override any attribute from the parent class

In Django, this isn’t permitted for model fields. If a non-abstract model base class has a field called author, you can’t create another model field or define an attribute called author in any class that inherits from that base class

This restriction doesn’t apply to model fields inherited from an abstract model. Such fields may be overridden with another field or value, or be removed by setting field_name = None

---
### Best practise 

Organizing models in a package
- The manage.py startapp command creates an application structure that includes a models.py file. 
    - if you have many models, organizing them in separate files may be useful

1. create a models package 
    - remove models.py and create a myapp/models/ directory with an \_\_init\_\_.py file 
    - create the files to store your models
    - import the models in the \_\_init\_\_.py file

For example, if you had organic.py and synthetic.py in the models directory:
in myapp/models/\_\_init\_\_.py
```
from .organic import Person
from .synthetic import Robot
```

Explicitly importing each model rather than using from .models import * has the advantages of not cluttering the namespace, making code more readable, and keeping code analysis tools useful

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Inheritance