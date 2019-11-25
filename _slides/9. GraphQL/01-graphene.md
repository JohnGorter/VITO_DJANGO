# Graphene

---
### Graphene

Graphene is a library that provides tools to implement a GraphQL API in Python using a code-first approach.

Instead of writing GraphQL Schema Definition Language (SDL), ypu write Python code to describe the data provided by your server

---
### Graphene (2)
Graphene features
- fully featured with integrations for the most popular web frameworks and ORMs. 
- produces schemas tha are fully compliant with the GraphQL spec 
-  provides tools and patterns for building a Relay-Compliant API as well

---
### Install Graphene
Installation requirements
- Python (2.7, 3.4, 3.5, 3.6, pypy)
- Graphene (2.0)

To install 
```
pip install "graphene>=2.0"
```

---
### An example in Graphene
Let’s build a basic GraphQL schema to say “hello” and “goodbye” in Graphene

Lets send a Query requesting only one Field, hello, and specify a value for the name Argument...
```
{
  hello(name: "friend")
}
```
we would expext
```
{
  "data": {
    "hello": "Hello friend!"
  }
}
```

---
### Creating a basic Schema
In Graphene, you can define a simple schema using the following code:
```
from graphene import ObjectType, String, Schema

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

schema = Schema(query=Query)
```

---
### Schema Definition Language (SDL)
In the GraphQL Schema Definition Language, we could describe the fields defined by our example code as show below.
```
type Query {
  hello(name: String = "stranger"): String
  goodbye: String
}
```

---
### Querying
Now we can start querying our Schema by passing a GraphQL query string to execute:
```
# we can query for our field (with the default argument)
query_string = '{ hello }'
result = schema.execute(query_string)
print(result.data['hello'])
# "Hello stranger"

# or passing the argument in the query
query_with_argument = '{ hello(name: "GraphQL") }'
result = schema.execute(query_with_argument)
print(result.data['hello'])
# "Hello GraphQL!"
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using Graphene


---
### Testing in Graphene
Automated testing is an extremely useful bug-killing tool for the modern developer 
You can use a collection of tests to solve, or avoid, a number of problems:

- when writing new code, use tests to validate your code works as expected
- when you’re refactoring or modifying old code, use tests to ensure your changes haven’t affected your application

---
### Testing in Graphene (2)
Testing a GraphQL application is a complex task, because a GraphQL application is made of
- schema definition
- schema validation
- permissions 
- field resolution

---
### Graphene test-execution framework 
Graphene test-execution framework allows you to:
- simulate GraphQL requests
- execute mutations
- inspect your application’s output 
- generally verify your code is doing what it should be doing

---
### Graphene Test Client
The test client is a Python class that acts as a dummy GraphQL client

Some of the things you can do with the test client are:
- simulate Queries and Mutations and observe the response
- test that a given query request is rendered by a given Django template

---
### A quick example
To use the test client
- instantiate graphene.test.Client 
- retrieve GraphQL responses

```
from graphene.test import Client

def test_hey():
    client = Client(my_schema)
    executed = client.execute('''{ hey }''')
    assert executed == {
        'data': {
            'hey': 'hello!'
        }
    }
```

---
### Execute parameters
You can also add extra keyword arguments to the execute method, such as context, root, variables, ...:
```
from graphene.test import Client

def test_hey():
    client = Client(my_schema)
    executed = client.execute('''{ hey }''', context={'user': 'Peter'})
    assert executed == {
        'data': {
            'hey': 'hello Peter!'
        }
    }
```

---
### Snapshot testing
As our APIs evolve, we need to know when our changes introduce any breaking changes that might break some of the clients of our GraphQL app.

However, writing tests and replicate the same response we expect from our GraphQL application can be tedious and repetitive task, and sometimes it’s easier to skip this process.

Because of that, we recommend the usage of SnapshotTest

---
### Snapshot testing(2)

SnapshotTest automatically creates the snapshots the first time the test is executed.

Here is a simple example on how our tests will look if we use pytest:
```
from snapshottest import TestCase

class APITestCase(TestCase):
    def test_api_me(self):
        client = Client(my_schema)
        self.assertMatchSnapshot(client.execute('''{ hey }'''))
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using Graphene tests


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Graphene tests

