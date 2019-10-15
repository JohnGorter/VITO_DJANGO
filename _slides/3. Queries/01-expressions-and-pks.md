# F Expressions and PK lookups

---
### F Expressions (1)

Filters can reference fields on the model
- what if you want to compare the value of a model field with another field on the same model?
- F expressions to allow such comparisons
- instances of F() act as a reference to a model field within a query


For example, to find a list of all blog entries that have had more comments than pingbacks
```
>>> from django.db.models import F
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks'))
```

---
### F Expressions (2)

Django supports the use of addition, subtraction, multiplication, division, modulo, and power arithmetic with F() objects, both with constants and with other F() objects 

To find all the blog entries with more than twice as many comments as pingbacks:
```
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
```
To find all the entries where the rating of the entry is less than the sum of the pingback count and comment count:
```
>>> Entry.objects.filter(rating__lt=F('n_comments') + F('n_pingbacks'))
```

---
### F Expressions (3)
You can also use the double underscore notation to span relationships in an F() object

An F() object with a double underscore will introduce any joins needed to access the related object

For example, to retrieve all the entries where the author’s name is the same as the blog name:
```
>>> Entry.objects.filter(authors__name=F('blog__name'))
```

---
### More F Expressions
For date and date/time fields, you can add or subtract a timedelta object

The following would return all entries that were modified more than 3 days after they were published:
```
>>> from datetime import timedelta
>>> Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))
```

The F() objects support bitwise operations by .bitand(), .bitor(), .bitrightshift(), and .bitleftshift()
For example
```
>>> F('somefield').bitand(16)
```

---
### The pk lookup shortcut
For convenience, Django provides a pk lookup shortcut, which stands for “primary key”.

In the example Blog model, the primary key is the id field, so these three statements are equivalent:
```
>>> Blog.objects.get(id__exact=14) # Explicit form
>>> Blog.objects.get(id=14) # __exact is implied
>>> Blog.objects.get(pk=14) # pk implies id__exact
```

---
### The pk lookup (2)

The use of pk isn’t limited to __exact queries – any query term can be combined with pk to perform a query on the primary key of a model:
```
# Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1,4,7])
```
```
# Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)
```

---
### pk across joins

pk lookups also work across joins. 

For example, these three statements are equivalent:
```
>>> Entry.objects.filter(blog__id__exact=3) # Explicit form
>>> Entry.objects.filter(blog__id=3)        # __exact is implied
>>> Entry.objects.filter(blog__pk=3)        # __pk implies __id__exact
```

---
### Escaping
The field lookups that equate to LIKE SQL statements (iexact, contains, icontains, startswith, istartswith, endswith and iendswith) will automatically escape the two special characters used in LIKE statements 
    – the percent sign
    - the underscore. (In a LIKE statement, the percent sign is a multiple-character wildcard and the underscore is a single-character wildcard)

This means things should work intuitively, so the abstraction doesn’t leak. 

For example, to retrieve all the entries that contain a percent sign, 
just use the percent sign as any other character:
```
>>> Entry.objects.filter(headline__contains='%')
```
Django takes care of the quoting for you; the resulting SQL will look something like this:
```
SELECT ... WHERE headline LIKE '%\%%';
```
Same goes for underscores

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
F Expressions
