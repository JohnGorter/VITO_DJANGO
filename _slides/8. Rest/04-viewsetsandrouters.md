# Viewsets and Routers

---
### ViewSets

ViewSets allows the developer to
- concentrate on modeling the state and interactions of the API
- leave the URL construction to be handled automatically, based on common conventions

ViewSets are almost the same thing as View classes except that 
- they provide operations such as read, or update
- not method handlers such as get or put


---
### ViewSet example
With ViewSets we van refactor our UserList and UserDetail views into a single UserViewSet

example
```
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

---
### ViewSet custom endpoints
You can use the @action decorator to implement custom endpoints
```
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def custommethod(self, request, *args, **kwargs):
        movie = self.get_object()
        return Response(movie)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

This time we've used the ModelViewSet class in order to get the complete set of default read and write operations

---
### ViewSet custom endpoints (2)
Some remarks
- custom actions with the @action decorator will respond to GET requests by default
- you can use the methods argument if we wanted an action that responded to POST requests
- the URLs for custom actions by default depend on the method name itself 
- if you want to change the way url should be constructed, you can include url_path as a decorator keyword argument

---
### Binding ViewSets to URLs explicitly
The handler methods only get bound to the actions when we define the URLConf, like always

In the snippets/urls.py file you have to bind the ViewSet classes into a set of concrete views
```
from movie.views import MovieViewSet, UserViewSet, api_root
from rest_framework import renderers

movies_list = MovieViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
movie_detail = MovieViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
movie_custommethod = MovieViewSet.as_view({
    'get': 'custommethod'
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('movies/', movies_list, name='movies-list'),
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('movies/<int:pk>/highlight/', movie_custommethod, name='movie_custommethod'),
])
```

---
### Using Routers
Because we're using ViewSet classes rather than View classes, we actually don't need to design the URL conf ourselves!

```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
```

---
### Trade-offs between views vs viewsets
Advantage ViewSet
- it helps ensure that URL conventions will be consistent across your API
- it minimizes the amount of code you need to write
- it allows you to concentrate on the interactions and representations your API provides rather than the specifics of the URL conf

Disadvantage ViewSet
- using viewsets is less explicit than building your views individually

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
ViewSets

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Creating ViewSets

