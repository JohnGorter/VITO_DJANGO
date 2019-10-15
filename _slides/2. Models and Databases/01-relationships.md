# Relationships

---
### Relationships

Three most common types of database relationships
- many-to-one
- many-to-many  
- one-to-one

---
### Many-to-one relationships
To define a many-to-one relationship, use django.db.models.ForeignKey
- by including it as a class attribute of your model

ForeignKey requires a positional argument
- the class to which the model is related

---
### Example
- a Manufacturer makes multiple cars but each Car only has one Manufacturer 

```
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```

---
### Many-to-many relationships
To define a many-to-many relationship, use ManyToManyField
- include it as a class attribute of your model

ManyToManyField requires a positional argument
- the class to which the model is related

---
### Example 
- a Topping can be on multiple pizzas and each Pizza has multiple toppings 

```
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```

It doesn’t matter which model has the ManyToManyField, but put it in one of the models, not both!

---
### Extra fields on m2m relationships
You can put extra fields on the intermediate model

The intermediate model is associated with the ManyToManyField using the through argument 

Example
```
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```


---
### How to add relations

You can use 
- add()
- create()
- set()

Have to specify through_defaults for any required fields

```
>>> beatles.members.add(john, through_defaults={'date_joined': date(1960, 8, 1)})
>>> beatles.members.create(name="George Harrison", through_defaults={'date_joined': date(1960, 8, 1)})
>>> beatles.members.set([john, paul, ringo, george], through_defaults={'date_joined': date(1960, 8, 1)})
```

---
### Deleting relations
The clear() method can be used to remove all many-to-many relationships 

```
>>> # Beatles have broken up
>>> beatles.members.clear()
>>> # Note that this deletes the intermediate model instances
>>> Membership.objects.all()
<QuerySet []>
```

---
### Querying Relationships
You can query using the attributes of the many-to-many-related model:

```
# Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
<QuerySet [<Group: The Beatles>]>
```
or
```
# Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
<QuerySet [<Person: Ringo Starr]>
```

---
### Other Examples

If you need to access a membership’s information
```
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

Or you can query the many-to-many reverse relationship from a Person 
```
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
```

---
### One-to-one relationships

To define a one-to-one relationship, use OneToOneField
- by including it as a class attribute of your model

This is most useful on the primary key of an object when that object “extends” another object in some way.

OneToOneField requires a positional argument
- the class to which the model is related

---
### Example One-To-one

```
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

---
### Field name restrictions
Django places some restrictions on model field names
- a field name cannot be a Python reserved word
- a field name cannot contain more than one underscore in a row
- a field name cannot end with an underscore

```
class Example(models.Model):
    pass = models.IntegerField() # 'pass' is a reserved word!
```


SQL reserved words, such as join, where or select, are allowed as model field name

---
### Custom field types
If one of the existing model fields cannot be used to fit your purposes, or if you wish to take advantage of some less common database column types, you can create your own field class

---
### Meta options
Give your model metadata by using an inner class Meta

```
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

Model metadata is “anything that’s not a field”, such as 
- ordering options (ordering)
- database table name (db_table)
- human-readable singular and plural names 

Adding class Meta to a model is completely optional

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Relationships

