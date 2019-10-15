# Complex Queries

---
### Complex Queries (1)
Keyword argument queries – in filter(), etc. – are “AND”ed together

If you need to execute more complex queries (for example, queries with OR statements), use Q objects

A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments 

These keyword arguments are specified as in “Field lookups” above

---
### Complex Queries (2)

For example, this Q object encapsulates a single LIKE query:
```
from django.db.models import Q
Q(question__startswith='What')
```

---
### Complex Queries (3)

Q objects can be combined using the & and | operators

When an operator is used on two Q objects, it yields a new Q object

This statement yields a single Q object that represents the “OR” of two "question__startswith" queries:
```
Q(question__startswith='Who') | Q(question__startswith='What')
```
This is equivalent to the following SQL WHERE clause:
```
WHERE question LIKE 'Who%' OR question LIKE 'What%'
```

---
### Complex Queries (4)
Q objects can be negated using the tilde operator, allowing for combined lookups that combine both a normal query and a negated (NOT) query

```
Q(question__startswith='Who') | [tilde]Q(pub_date__year=2005)
```

---
### Complex Queries (5)
Each lookup function that takes keyword-arguments (e.g. filter(), exclude(), get()) can also be passed one or more Q objects as positional (not-named) arguments

If you provide multiple Q object arguments to a lookup function, the arguments will be “AND”ed together

For example:
```
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```
this roughly translates into the SQL:
```
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```

---
### Complex Queries
Lookup functions can mix the use of Q objects and keyword arguments

All arguments provided to a lookup function (be they keyword arguments or Q objects) are “AND”ed together

If a Q object is provided, it must precede the definition of any keyword arguments. 

For example
```
Poll.objects.get(Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),question__startswith='Who')
```
would be a valid query, equivalent to the previous example, but
```
# INVALID QUERY
Poll.objects.get(question__startswith='Who',Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
```
would not be valid

---
### Comparing objects
To compare two model instances, just use the standard Python comparison operator, the double equals sign: ==

Behind the scenes, that compares the primary key values of two models

the following two statements are equivalent
```
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```

---
### Comparing objects
Comparisons will always use the primary key, whatever it’s called. 

For example, if a model’s primary key field is called name, these two statements are equivalent:
```
>>> some_obj == other_obj
>>> some_obj.name == other_obj.name
```

---
### Bulk delete
Every QuerySet has a delete() method, which deletes all members of that QuerySet

For example, this deletes all Entry objects with a pub_date year of 2005:
```
>>> Entry.objects.filter(pub_date__year=2005).delete()
(5, {'webapp.Entry': 5})
```
---
### Cascade delete
When Django deletes an object, by default it emulates the behavior of the SQL constraint ON DELETE CASCADE 
– any objects which had foreign keys pointing at the object to be deleted will be deleted along with it 

For example:
```
b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
b.delete()
```

This cascade behavior is customizable via the on_delete argument to the ForeignKey

---
### Delete method
The delete() method is the only QuerySet method that is not exposed on a Manager itself

This is a safety mechanism to prevent you from accidentally requesting Entry.objects.delete()
 
If you do want to delete all the objects, then you have to explicitly request a complete query set:
```
Entry.objects.all().delete()
```

---
### Copying model instances
Although there is no built-in method for copying model instances, it is possible to easily create new instance with all fields’ values copied
- just set pk to None 

example:
```
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2
```

---
### Updating multiple objects at once (1)
Sometimes you want to set a field to a particular value for all the objects in a QuerySet
- use the update() method
```
# Update all the headlines with pub_date in 2007.
Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
```

---
### Updating multiple objects at once (2)

You can only set non-relation fields and ForeignKey fields using this method
- to update a non-relation field, provide the new value as a constant
- to update ForeignKey fields, set the new value to be the new model instance you want to point to

```
>>> b = Blog.objects.get(pk=1)
# Change every Entry so that it belongs to this Blog.
>>> Entry.objects.all().update(blog=b)
```

The update() method is applied instantly and returns the number of rows matched by the query

---
### Updating multiple objects at once (3) 
The update() method is converted directly to an SQL statement

It is a bulk operation for direct updates
- it doesn’t run any save() methods on your models
- it doesn't emit the pre_save or post_save signals 
- it doesn't honor the auto_now field option

If you want to save every item in a QuerySet and make sure that the save() method is called on each instance, loop over them and call save():
```
for item in my_queryset:
    item.save()
```

---
### Updating multiple objects at once (4) 
Calls to update can also use F expressions

This is especially useful for incrementing counters based upon their current value

```
>>> Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)
```

---
### Updating multiple objects at once (5) 
Unlike F() objects in filter and exclude clauses, you can’t introduce joins when you use F() objects in an update – you can only reference fields local to the model being updated

If you attempt to introduce a join with an F() object, a FieldError is raised:
```
# This will raise a FieldError
>>> Entry.objects.update(headline=F('blog__name'))
```

---
### Related objects
When you define a relationship in a model (i.e., a ForeignKey, OneToOneField, or ManyToManyField), instances of that model will have a convenient API to access the related object(s)

for example, an Entry object e can get its associated Blog object by accessing the blog attribute: e.blog

Django also creates API accessors for the “other” side of the relationship 
– a Blog object b has access to a list of all related Entry objects via the entry_set attribute: b.entry_set.all()


---
### One-to-many relationships (1)

If a model has a ForeignKey, instances of that model will have access to the related (foreign) object via a simple attribute of the model

Example:
```
>>> e = Entry.objects.get(id=2)
>>> e.blog # Returns the related Blog object.
```

---
### One-to-many relationships (2)
You can get and set via a foreign-key attribute. As you may expect, changes to the foreign key aren’t saved to the database until you call save()

Example
```
>>> e = Entry.objects.get(id=2)
>>> e.blog = some_blog
>>> e.save()
```

---
### One-to-many relationships (3)
If a ForeignKey field has null=True set (i.e., it allows NULL values), you can assign None to remove the relation 

Example
```
>>> e = Entry.objects.get(id=2)
>>> e.blog = None
>>> e.save() # "UPDATE blog_entry SET blog_id = NULL ...;"
```

---
### Forward access cache
Forward access to one-to-many relationships is cached the first time the related object is accessed 

Subsequent accesses to the foreign key on the same object instance are cached 

Example
```
>>> e = Entry.objects.get(id=2)
>>> print(e.blog)  # Hits the database to retrieve the associated Blog.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
```
---
### select_related()
the select_related() QuerySet method recursively prepopulates the cache of all one-to-many relationships ahead of time. 

Example:
```
>>> e = Entry.objects.select_related().get(id=2)
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
```

--
### Following relationships “backward”
If a model has a ForeignKey, instances of the foreign-key model will have access to a Manager that returns all instances of the first model

By default, this Manager is named FOO_set, where FOO is the source model name, lowercased

This Manager returns QuerySets, which can be filtered and manipulated as described in the “Retrieving objects” section above

Example:
```
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.all() # Returns all Entry objects related to Blog
# b.entry_set is a Manager that returns QuerySets.
>>> b.entry_set.filter(headline__contains='Lennon')
>>> b.entry_set.count()
```

---
### Override set names
You can override the FOO_set name by setting the related_name parameter in the ForeignKey definition

For example, if the Entry model was altered to 
```
blog = ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')
```
the above example code would look like this:
```
>>> b = Blog.objects.get(id=1)
>>> b.entries.all() # Returns all Entry objects related to Blog.
# b.entries is a Manager that returns QuerySets.
>>> b.entries.filter(headline__contains='Lennon')
>>> b.entries.count()
```

---
### Additional methods for relation objects
In addition to the QuerySet methods defined in “Retrieving objects” above, the ForeignKey Manager has additional methods used to handle the set of related objects

- add(obj1, obj2, ...): adds the specified model objects to the related object set.
- create(**kwargs): creates a new object, saves it and puts it in the related object set. Returns the newly created object.
- remove(obj1, obj2, ...): removes the specified model objects from the related object set.
- clear(): removes all objects from the related object set.
- set(objs): replace the set of related objects.
To assign the members of a related set, use the set() method with an iterable of object instances. 

For example, if e1 and e2 are Entry instances:
```
b = Blog.objects.get(id=1)
b.entry_set.set([e1, e2])
```

---
### Many-to-many relationships (1)
Both ends of a many-to-many relationship get automatic API access to the other end

The API works similar to a “backward” one-to-many relationship, above

One difference is in the attribute naming 
- the model that defines the ManyToManyField uses the attribute name of that field itself - the “reverse” model uses the lowercased model name of the original model, plus '_set' (just like reverse one-to-many relationships).

An example makes this easier to understand:
```
e = Entry.objects.get(id=3)
e.authors.all() # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains='John')

a = Author.objects.get(id=5)
a.entry_set.all() # Returns all Entry objects for this Author
```

---
### Many-to-many relationships (2)
Like ForeignKey, ManyToManyField can specify related_name

In the above example, if the ManyToManyField in Entry had specified related_name='entries', then each Author instance would have an entries attribute instead of entry_set

---
### Many-to-many relationships (3)

Another difference from one-to-many relationships is that in addition to model instances, the add(), set(), and remove() methods on many-to-many relationships accept primary key values. 

For example, if e1 and e2 are Entry instances, then these set() calls work identically:
```
a = Author.objects.get(id=5)
a.entry_set.set([e1, e2])
a.entry_set.set([e1.pk, e2.pk])
```

---
### One-to-one relationships (1)
Instances of that model will have access to the related object via a simple attribute of the model.

For example:
```
class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()

ed = EntryDetail.objects.get(id=2)
ed.entry # Returns the related Entry object.
```

---
### One-to-one relationships (2)
The related model in a one-to-one relationship also has access to a Manager object, but that Manager represents a single object, rather than a collection of objects:
```
e = Entry.objects.get(id=2)
e.entrydetail # re
```

---
### How are the backward relationships possible?
Other object-relational mappers require you to define relationships on both sides 

The Django developers believe this is a violation of the DRY (Don’t Repeat Yourself) principle, so Django only requires you to define the relationship on one end

When Django starts, it imports each application listed in INSTALLED_APPS, and then the models module inside each application. 

Whenever a new model class is created, Django adds backward-relationships to any related models. If the related models haven’t been imported yet, Django keeps tracks of the relationships and adds them when the related models eventually are imported.

For this reason, it’s particularly important that all the models you’re using be defined in applications listed in INSTALLED_APPS. Otherwise, backwards relations may not work properly.


---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Complex Queries
