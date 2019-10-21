# Requests and Responses

---
### Requests and Responses


DRF introduces a Request object that extends the regular HttpRequest with
- request.data attribute
- request.POST only handles 'POST' method while request.data handles 'POST', 'PUT' and 'PATCH' methods

DRF introduces an extended Response object
- uses content negotiation to determine the correct content type to return to the client


---
### API Views

DRF provides two wrappers you can use to write API views
- the @api_view decorator for working with function based views
- the APIView class for working with class-based views

These wrappers provide a few bits of functionality such as 
- making sure you receive Request instances in your view
- adding context to Response objects so that content negotiation can be performed

---
### Example API View

example

```
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie.models import Movie
from Movie.serializers import MovieSerializer


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---
### Example API View detail
example detail view
```
@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---
### Example API View detail
example url config
```
from django.urls import path
from movie import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:pk>/', views.movie_detail),
]
```
and in the root urlconf
```
from django.urls import path, include

urlpatterns = [
    path('', include('movies.urls')),
]
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
API View function

---
### Optional format suffixes 
Format suffixes make URLs that explicitly refer to a given format
- http://example.com/api/items/4.json

add a format keyword argument 
```
def movie_list(request, format=None):
...
def movie_detail(request, pk, format=None):
```
and update the urls.py
```
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from movies import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:pk>', views.movie_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Format suffixes

---
### Class-based Views

You can also write our API views using class-based views, rather than function based views
- a powerful pattern that allows for reuse of common functionality
- helps keep the code DRY

---
### Class-based Views

Example of a class based view
```
class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---
### Class-based Views
```
class MovieDetail(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```


---
### Class-based views
And update the urls.py
```
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

---
### Using mixins
One of the big advantage of using class-based views is
- it allows us to easily compose reusable bits of behaviour
- generic API View crud implementations

---
### Using mixins example

```
from movies.models import Movie
from movies.serializers import MovieSerializer
from rest_framework import mixins
from rest_framework import generics

class MoviesList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

View uses GenericAPIView, ListModelMixin and CreateModelMixin
- base class provides the core functionality
- the mixin classes provide the .list() and .create() actions
- the get and post methods are explicitly bound to the appropriate actions

---
### Using generic class-based views
Using the mixin classes gives us slightly less code than before, but we can go one step further. 

DRF provides a set of already mixed-in generic views 
```
from movies.models import Movie
from movies.serializers import MovieSerializer
from rest_framework import generics

class MoviesList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = MovieSerializer

class MoviesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = MovieSerializer
```



---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Generics based views

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Api Views

