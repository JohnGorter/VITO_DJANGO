# Queries

---
### Creating Objects

A model class represents a database table, and an instance of that class represents a particular record in the database table

To create an object
- instantiate it using keyword arguments to the model class
- call save() to save it to the database

---
### Example

```
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```

This performs an INSERT SQL statement behind the scenes
- Django doesn’t hit the database until you explicitly call save()
- To create and save an object in a single step, use the create() method

---
### Saving ForeignKey fields
Updating a ForeignKey field works exactly the same way as saving a normal field 
– simply assign an object of the right type to the field

Example
```
>>> from blog.models import Blog, Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog
>>> entry.save()
```

---
### Saving ManyToManyField fields

use the add() method on the field to add a record to the relation

Example
```
>>> from blog.models import Author
>>> joe = Author.objects.create(name="Joe")
>>> entry.authors.add(joe)
```
---
### Multiple records
To add multiple records to a ManyToManyField in one go, 
include multiple arguments in the call to add()

```
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
```

---
### Retrieving objects (1)
To retrieve objects from your database, construct a QuerySet via a Manager on your model class

A QuerySet represents a collection of objects from your database
- It can have zero, one or many filters
- a filter is a limiting clause such as WHERE or LIMIT

---
### Retrieving objects (2)
You get a QuerySet by using your model’s Manager
- it’s called 'objects' by default

```
>>> Blog.objects
<django.db.models.manager.Manager object at ...>
>>> b = Blog(name='Foo', tagline='Bar')
>>> b.objects
Traceback:
    ...
AttributeError: "Manager isn't accessible via Blog instances."
```

---
### Retrieving all objects
The simplest way to retrieve objects from a table is to get all of them
```
>>> all_entries = Entry.objects.all()
```
The all() method returns a QuerySet of all the objects in the database.

---
### Retrieving with filters
You can refine the initial QuerySet, by adding filter conditions

The two most common ways to refine a QuerySet are:
- filter(**kwargs)
Returns a new QuerySet containing objects that match the given lookup parameters
- exclude(**kwargs)
Returns a new QuerySet containing objects that do not match the given lookup parameters

For example
```
Entry.objects.filter(pub_date__year=2006) 
```

---
### Chaining filters
The result of refining a QuerySet is itself a QuerySet
- it’s possible to chain refinements together

Example
```
>>> Entry.objects.filter(headline__startswith='What')
    .exclude(pub_date__gte=datetime.date.today())
    .filter(pub_date__gte=datetime.date(2005, 1, 30))
```

---
### Filtered QuerySets are unique
Each time you refine a QuerySet, you get a brand-new QuerySet
 
Each refinement creates a separate and distinct QuerySet that can be stored, used and reused

Example:
```
>>> q1 = Entry.objects.filter(headline__startswith="What")
>>> q2 = q1.exclude(pub_date__gte=datetime.date.today())
>>> q3 = q1.filter(pub_date__gte=datetime.date.today())
```

---
### QuerySets are lazy
The act of creating a QuerySet doesn’t involve any database activity

You can stack filters together, Django won’t actually run the query until the QuerySet is evaluated

```
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)
```

---
### Retrieving a single object

If you know there is only one object that matches your query, you can use the get() 
```
>>> one_entry = Entry.objects.get(pk=1)
```

If there is no Entry object with a primary key of 1, Django will raise Entry.DoesNotExist
If more than one item matches the get() query, it will raise MultipleObjectsReturned

---
### Other QuerySet methods
QuerySet API Reference for a complete list of all the various QuerySet methods

https://docs.djangoproject.com/en/2.2/ref/models/querysets/#queryset-api

---
### Limiting QuerySets (1)
Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results
- this is the equivalent of SQL’s LIMIT and OFFSET clauses

For example, this returns the first 5 objects (LIMIT 5):
```
>>> Entry.objects.all()[:5]
```
This returns the sixth through tenth objects (OFFSET 5 LIMIT 5):
```
>>> Entry.objects.all()[5:10]
```

Negative indexing (i.e. Entry.objects.all()[-1]) is not supported

Slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query

---
### Limiting QuerySets (2)

An exception is if you use the “step” parameter of Python slice syntax. 

For example, this would execute the query in order to return a list of every second object of the first 10:
```
>>> Entry.objects.all()[:10:2]
```

---
### Limiting QuerySets (3)

To retrieve a single object rather than a list (e.g. SELECT foo FROM bar LIMIT 1), use a simple index instead of a slice. 

This returns the first Entry in the database, after ordering entries alphabetically by headline:
```
>>> Entry.objects.order_by('headline')[0]
```

This is roughly equivalent to:
```
>>> Entry.objects.order_by('headline')[0:1].get()
```

---
### Field lookups (SQL WHERE)

Basic lookups keyword arguments take the form field__lookuptype=value
- it is the meat of an SQL WHERE clause
```
>>> Entry.objects.filter(pub_date__lte='2006-01-01')
```
translates (roughly) into the following SQL:
```
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';
```

---
### Foreign key lookups
The field specified in a lookup has to be the name of a model field!

There’s one exception though, in case of a ForeignKey you can specify the field name suffixed with _id. 

In this case, the value parameter is expected to contain the raw value of the foreign model’s primary key.

```
>>> Entry.objects.filter(blog_id=4)
```

---
### Exact field lookups (1)
- exact: an “exact” match
```
>>> Entry.objects.get(headline__exact="Cat bites dog")
```
Would generate SQL along these lines:
```
SELECT ... WHERE headline = 'Cat bites dog';
```

---
### Exact field lookups (2)
If you don’t provide a lookup type 
– that is, if your keyword argument doesn’t contain a double underscore
– the lookup type is assumed to be exact

For example, the following two statements are equivalent:
```
>>> Blog.objects.get(id__exact=14)  # Explicit form
>>> Blog.objects.get(id=14)         # __exact is implied
```


This is for convenience, because exact lookups are the common case

---
### IExact field lookups

- iexact: a case-insensitive match
```
>>> Blog.objects.get(name__iexact="beatles blog")
```
Would match a Blog titled "Beatles Blog", "beatles blog", or even "BeAtlES blOG"

---
### Contains field lookups (SQL LIKE)

- contains: a case-sensitive containment test
```
Entry.objects.get(headline__contains='Lennon')
```
Roughly translates to this SQL:
```
SELECT ... WHERE headline LIKE '%Lennon%';
```

Note this will match the headline 'Today Lennon honored' but not 'today lennon honored'

There’s also a case-insensitive version, icontains


---
### StartsWith and EndsWith field lookups

- starts-with and ends-with search: search
- istartswith and iendswith: search case-insensitive

---
### Lookups that span relationships (SQL JOINS)
To span a relationship, just use the field name of related fields across models, 
separated by double underscores, until you get to the field you want

Example retrieving all Entry objects with a Blog whose name is 'Beatles Blog':
```
>>> Entry.objects.filter(blog__name='Beatles Blog')
```

This spanning can be as deep as you’d like

---
### “reverse” relationship

It works backwards, too. To refer to a “reverse” relationship, just use the lowercase name of the model.

This example retrieves all Blog objects which have at least one Entry whose headline contains 'Lennon':
```
>>> Blog.objects.filter(entry__headline__contains='Lennon')
```

---
### Another Example

To select all blogs that contain entries with both “Lennon” in the headline and that were published in 2008 (the same entry satisfying both conditions), we would write:
```
Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
```

To select all blogs that contain an entry with “Lennon” in the headline as well as an entry that was published in 2008, we would write:
```
Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
```


---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Queries



