# Graphene Django

---
### Graphene Django

> With Graphene, we do not have to use GraphQL's syntax to create a schema, we only use Python! 


---
### Context

Consider the following schema
```
type Actor { id: ID!  name: String! }
type Movie { id: ID!  title: String!  actors: [Actor] year: Int! }

type Query {
  actor(id: ID!): Actor
  movie(id: ID!): Movie
  actors: [Actor]
  movies: [Movie]
}

input ActorInput { id: ID name: String! }
input MovieInput { id: ID title: String actors: [ActorInput] year: Int }

type ActorPayload { ok: Boolean actor: Actor }
type MoviePayload { ok: Boolean movie: Movie }

type Mutation {
  createActor(input: ActorInput) : ActorPayload
  createMovie(input: MovieInput) : MoviePayload
  updateActor(id: ID!, input: ActorInput) : ActorPayload
  updateMovie(id: ID!, input: MovieInput) : MoviePayload
}
```

What do you read from this schema?

---
### Application Setup

```
$ mkdir django_graphql_movies
$ cd django_graphql_movies/
$ python3 -m venv env
```
activate venv
```
$ . env/bin/activate
```

---
### Application Setup (2)
```
$ pip install Django
$ pip install graphene_django
```

then create the Django project
```
$ django-admin.py startproject django_graphql_movies .
$ cd django_graphql_movies/
$ django-admin.py startapp movies
```

---
### Application Setup (3)
sync the databases
```
# First return to the project's directory
$ cd ..
# And then run the migrate command
$ python manage.py migrate
```

---
### Lets make the model

We already know about models...

So in django_graphql_movies/movies/models.py
```
from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField()
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('title',)
```

---
### App registration
We can now register our movies app within the project
```
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'django.contrib.staticfiles',
    'django_graphql_movies.movies', # <-
]
```
Be sure to migrate your database to keep it in sync with our code changes
```
$ python manage.py makemigrations
$ python manage.py migrate
```

---
### Loading Test Data

Let's load some data into our database, save the following JSON as movies.json in your project's root directory:
```
[
  {
    "model": "movies.actor",
    "pk": 1,
    "fields": { "name": "Michael B. Jordan" }
  },
  {
    "model": "movies.actor",
    "pk": 2,
    "fields": { "name": "Sylvester Stallone" }
  },
  {
    "model": "movies.movie",
    "pk": 1,
    "fields": { "title": "Creed", "actors": [1, 2], "year": "2015" }
  }
]
```
Run the following command to load the test data:
```
$ python manage.py loaddata movies.json
```


---
### Making Queries
In our movies app folder, create a new schema.py file

Define our GraphQL types:
```
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django_graphql_movies.movies.models import Actor, Movie

# Create a GraphQL type for the actor model
class ActorType(DjangoObjectType):
    class Meta:
        model = Actor

# Create a GraphQL type for the movie model
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
```

To create a GraphQL type, specify which Django model has the properties for the API

---
### Making Queries (2)
In the same file, add the following code to create the Query type:
```
# Create a Query type
class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies= graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Actor.objects.get(pk=id)
        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Movie.objects.get(pk=id)
        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()
```

---
### Resolvers

The four methods we created in the Query class are called resolvers
- connect the queries in the schema to actual actions done by the database


---
### Making Mutations
Add the following to schema.py
```
# Create Input Object Types
class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()
```

They are simple classes that define what fields can be used to change data in the API.

---
### Making Mutations (2)
Creating mutations require a bit more work than creating queries.
Add the mutations for actors:
```
# Create mutations for actors
class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)

class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)
```

---
### Making Mutations (3)
Recall the signature for the createActor mutation when we designed our schema:
-  createActor(input: ActorInput) : ActorPayload
    - the class' name corresponds to the GraphQL's query name
    - the inner Arguments class properties correspond to the input arguments for the mutator
    - the ok and actor properties make up the ActorPayload

---
### Making Mutations (4)

Now let's add the mutation for movies
```
# Create mutations for movies
class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actors = []
        for actor_input in input.actors:
          actor = Actor.objects.get(pk=actor_input.id)
          if actor is None:
            return CreateMovie(ok=False, movie=None)
          actors.append(actor)
        movie_instance = Movie(
          title=input.title,
          year=input.year
          )
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
              actor = Actor.objects.get(pk=actor_input.id)
              if actor is None:
                return UpdateMovie(ok=False, movie=None)
              actors.append(actor)
            movie_instance.title=input.title
            movie_instance.year=input.yearce.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)
```

When working with many-to-many relationships, save related data after object is saved

---
### Making Mutations (5)
To complete our mutations, we create the Mutation type:
```
class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
```

---
### Making the Schema
Map the queries and mutations to our application's API
```
schema = graphene.Schema(query=Query, mutation=Mutation)
```

---
### Registering the Schema
For our API to work, we need to make a schema available project wide (one level up).

Create a new schema.py file in django_graphql_movies/ and add the following:
```
import graphene
import django_graphql_movies.movies.schema

class Query(django_graphql_movies.movies.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(django_graphql_movies.movies.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

---
### Registering the Schema (2)
Now register with graphene and tell it to use our schema

Open django_graphql_movies/settings.py 
- add 'graphene_django' as the first item in the INSTALLED_APPS.

In the same file add the following code a couple of new lines below the INSTALLED_APPS:
```
GRAPHENE = {
    'SCHEMA': 'django_graphql_movies.schema.schema'
}
```

---
### Registering the route
GraphQL APIs are reached via one endpoint, /graphql. 
Register that route, or rather view, in Django.

Open django_graphql_movies/urls.py and change the file contents to
```
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django_graphql_movies.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
```


---
### Testing Our API
To test our API, let's run the project and then go to the GraphQL endpoint
```
$ python manage.py runserver
```
Once your server is running head to
```
http://127.0.0.1:8000/graphql/
```
You'll encounter GraphiQL - a built in IDE to run your queries!

---
### Writing Queries
We now can query our database
```
query getActors {
  actors {
    id
    name
  }
}
```
or 
```
query getMovie {
  movie(id: 1) {
    id
    title
    actors {
      id
      name
    }
  }
}
```

---
### Writing Mutations
Mutations follow a similar style as queries
```
mutation createActor {
  createActor(input: {
    name: "Tom Hanks"
  }) {
    ok
    actor {
      id
      name
    }
  }
}
```
Notice how the input parameter corresponds to the input properties of the Arguments classes we created earlier

---
### Writing Mutations (2)
And to create a movie
```
mutation createMovie {
  createMovie(input: {
    title: "Cast Away",
    actors: [
      {
        id: 3
      }
    ]
    year: 1999
  }) {
    ok
    movie{
      id
      title
      actors {
        id
        name
      }
      year
    }
  }
}
```

---
### Writing Mutations (3)
Unfortunately, we just made a mistake. "Cast Away" came out in the year 2000!

To do an update 
```
mutation updateMovie {
  updateMovie(id: 2, input: {
    title: "Cast Away",
    actors: [
      {
        id: 3
      }
    ]
    year: 2000
  }) {
    ok
    movie{
      id
      title
      actors {
        id
        name
      }
      year
    }
  }
}
```

---
### Disable GraphiQL
GraphiQL is very useful during development
- it's standard practice to disable in production 
- it may allow an external developer too much insight into the API

To disable GraphiQL:
- simply edit django_graphql_movies/urls.py 
    - replace path('graphql/', GraphQLView.as_view(graphiql=True)), 
    - with path('graphql/', GraphQLView.as_view(graphiql=False)),

---
### Communicating via POST
An application communicating with your API would send POST requests to the /graphql endpoint

Before we can make POST requests from outside the Django site, change django_graphql_movies/urls.py:
```
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django_graphql_movies.schema import schema
from django.views.decorators.csrf import csrf_exempt # <------ added

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

Django comes built-in with CSRF (Cross-Site Request Forgery) protection
- it has measures to prevent incorrectly authenticated users of the site from performing potentially malicious actions

---
### Communicating via POST (2)
In terminal we could enter
```
$ curl \
  -X POST \
  -H "Content-Type: application/json" \
  --data '{ "query": "{ actors { name } }" }' \
  http://127.0.0.1:8000/graphql/
```
the response would be
```
{"data":{"actors":[{"name":"Michael B. Jordan"},{"name":"Sylvester Stallone"},{"name":"Tom Hanks"}]}}
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using graphene_django 

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Using graphene_django

