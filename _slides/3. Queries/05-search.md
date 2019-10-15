# Search

---
### Search
> search some data in the database with user input

---
### Standard textual queries
Text-based fields have a selection of simple matching operations. For example, you may wish to allow lookup up an author like so:
```
>>> Author.objects.filter(name__contains='Terry')
[<Author: Terry Gilliam>, <Author: Terry Jones>]
```

This is a very fragile solution as it requires the user to know an exact substring of the author’s name. A better approach could be a case-insensitive match (icontains), but this is only marginally better.

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Aggregations
