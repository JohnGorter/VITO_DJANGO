# Aggregations

---
### Aggregation
> To retrieve values that are derived by summarizing or aggregating a collection of objects

---
### Generating aggregates over a QuerySet (1)
To calculate summary values over the objects that belong to this QuerySet, use an aggregate() clause onto the QuerySet

```
>>> from django.db.models import Avg
>>> Book.objects.all().aggregate(Avg('price'))
{'price__avg': 34.35}
```
or 
```
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': 34.35}
```
The argument to the aggregate() clause describes the aggregate value that we want to compute


---
### Generating aggregates over a QuerySet (2)
If you want to generate more than one aggregate, you just add another argument to the aggregate() clause. 

So, if we also wanted to know the maximum and minimum price of all books
```
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}
```

---
### Generating aggregates for each item in a QuerySet (1)
Per-object summaries can be generated using the annotate() clause. 

When an annotate() clause is specified, each object in the QuerySet will be annotated with the specified values.

For example, to annotate books with the number of authors
```
# Build an annotated queryset
>>> from django.db.models import Count
>>> q = Book.objects.annotate(Count('authors'))
# Interrogate the first object in the queryset
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].authors__count
2
# Interrogate the second object in the queryset
>>> q[1]
<Book: Practical Django Projects>
>>> q[1].authors__count
1
```

---
### Annotate name
As with aggregate(), the name for the annotation is automatically derived from the name of the aggregate function and the name of the field being aggregated. 

You can override this default name by providing an alias when you specify the annotation:
```
>>> q = Book.objects.annotate(num_authors=Count('authors'))
>>> q[0].num_authors
2
>>> q[1].num_authors
1
```


---
### Difference between annotate and aggregate
Unlike aggregate(), annotate() is not a terminal clause

The output of the annotate() clause is a QuerySet
- this QuerySet can be modified using any other QuerySet operation
    - including filter(), order_by(), or even additional calls to annotate()


---
### Combining multiple aggregations (1)
Combining multiple aggregations with annotate() will yield the wrong results because joins are used instead of subqueries
```
>>> book = Book.objects.first()
>>> book.authors.count()
2
>>> book.store_set.count()
3
>>> q = Book.objects.annotate(Count('authors'), Count('store'))
>>> q[0].authors__count
6
>>> q[0].store__count
6
```

---
### Combining multiple aggregations (2)
For most aggregates, there is no way to avoid this problem, however, the Count aggregate has a distinct parameter that may help:
```
>>> q = Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))
>>> q[0].authors__count
2
>>> q[0].store__count
3
```

---
### Joins and aggregates (1)
Suppose the value you want to aggregate belongs to a model that is related to the model you are querying

 Django will allow you to use the same double underscore notation that is used when referring to related fields in filters

For example, to find the price range of books offered in each store, you could use the annotation
```
>>> from django.db.models import Max, Min
>>> Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
```

---
### Joins and aggregates (2)
The same rules apply to the aggregate() clause. If you wanted to know the lowest and highest price of any book that is available for sale in any of the stores, you could use the aggregate:
```
>>> Store.objects.aggregate(min_price=Min('books__price'), max_price=Max('books__price'))
```

---
### Joins and aggregates (3)
Join chains can be as deep as you require. 

For example, to extract the age of the youngest author of any book available for sale, you could issue the query:
```
>>> Store.objects.aggregate(youngest_age=Min('books__authors__age'))
```

---
### Aggregations and other QuerySet clauses (1)
Aggregates can also participate in filters. Any filter() (or exclude()) applied to normal model fields will have the effect of constraining the objects that are considered for aggregation.

When used with an annotate() clause, a filter has the effect of constraining the objects for which an annotation is calculated. 

For example, you can generate an annotated list of all books that have a title starting with “Django” using the query:
```
>>> from django.db.models import Avg, Count
>>> Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))
```

---
### Aggregations and other QuerySet clauses (2)
When used with an aggregate() clause, a filter has the effect of constraining the objects over which the aggregate is calculated. 

For example, you can generate the average price of all books with a title that starts with “Django” using the query:
```
>>> Book.objects.filter(name__startswith="Django").aggregate(Avg('price'))
```

---
### Filtering on annotations (1)
Annotated values can also be filtered. The alias for the annotation can be used in filter() and exclude() clauses in the same way as any other model field.

For example, to generate a list of books that have more than one author, you can issue the query
```
>>> Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)
```
This query generates an annotated result set, and then generates a filter based upon that annotation

---
### Filtering on annotations (2)
If you need two annotations with two separate filters you can use the filter argument with any aggregate. For example, to generate a list of authors with a count of highly rated books:
```
>>> highly_rated = Count('book', filter=Q(book__rating__gte=7))
>>> Author.objects.annotate(num_books=Count('book'), highly_rated_books=highly_rated)
```

Each Author in the result set will have the num_books and highly_rated_books attributes

---
### Order of annotate() and filter() clauses (1)
Ordering does matter

When an annotate() clause is applied to a query, the annotation is computed over the state of the query up to the point where the annotation is requested. The practical implication of this is that filter() and annotate() are not commutative operations

Given:

Publisher A has two books with ratings 4 and 5.
Publisher B has two books with ratings 1 and 4.
Publisher C has one book with rating 1.

---
### Order of annotate() and filter() clauses (2)
Here’s an example with the Count aggregate:
```
>>> a, b = Publisher.objects.annotate(num_books=Count('book', distinct=True)).filter(book__rating__gt=3.0)
>>> a, a.num_books
(<Publisher: A>, 2)
>>> b, b.num_books
(<Publisher: B>, 2)

>>> a, b = Publisher.objects.filter(book__rating__gt=3.0).annotate(num_books=Count('book'))
>>> a, a.num_books
(<Publisher: A>, 2)
>>> b, b.num_books
(<Publisher: B>, 1)
```

Both queries return a list of publishers that have at least one book with a rating exceeding 3.0, hence publisher C is excluded.

---
### order_by()
Annotations can be used as a basis for ordering. When you define an order_by() clause, the aggregates you provide can reference any alias defined as part of an annotate() clause in the query.

For example, to order a QuerySet of books by the number of authors that have contributed to the book, you could use the following query:
```
>>> Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
```

---
### values()
Ordinarily, annotations are generated on a per-object basis 
- an annotated QuerySet will return one result for each object in the original QuerySet

Instead of returning an annotated result for each result in the original QuerySet, the original results are grouped according to the unique combinations of the fields specified in the values() clause

An annotation is then provided for each unique group; the annotation is computed over all members of the group

---
### values() (2)
For example, consider an author query that attempts to find out the average rating of books written by each author:
```
>>> Author.objects.annotate(average_rating=Avg('book__rating'))
```

This will return one result for each author in the database, annotated with their average book rating.

However...
---
### values() (3)
...the result will be slightly different if you use a values() clause:
```
>>> Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
```

In this example, the authors will be grouped by name, so you will only get an annotated result for each unique author name.

---
### Aggregating annotations
You can also generate an aggregate on the result of an annotation. When you define an aggregate() clause, the aggregates you provide can reference any alias defined as part of an annotate() clause in the query

For example, if you wanted to calculate the average number of authors per book you first annotate the set of books with the author count, then aggregate that author count, referencing the annotation field:
```
>>> from django.db.models import Avg, Count
>>> Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))
{'num_authors__avg': 1.66}
```


---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Aggregations
