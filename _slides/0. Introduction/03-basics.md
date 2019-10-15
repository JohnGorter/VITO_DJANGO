# Basics

---
### Django Apps
In the Django philosophy we have two important concepts
- app: is a Web application that does something
    - an app usually is composed of a set of models (database tables), views, templates, tests

- project: is a collection of configurations and apps
    - one project can be composed of multiple apps, or a single app
        
It’s important to note that you can’t run a Django app without a project. 

Simplewebsites like a blog can be written entirely inside a single app, which could be named blog or weblog for example

---
### Creating an app
To create our first app, go to the directory where the manage.py file is and execute the following command
```
django-admin startapp boards
```

---
### Createing an app (2)
This will give us the following directory structure:
```
myproject/
|-- myproject/
| |-- boards/   <-- our new django app!
| | |-- migrations/
| | |     +-- __init__.py 
| | |-- __init__.py
| | |-- admin.py
| | |-- apps.py
| | |-- models.py
| | |-- tests.py
| | +-- views.py
| |-- myproject/
| | |-- __init__.py
| | |-- settings.py 
| | |-- urls.py
| | |-- wsgi.py
| +-- manage.py
+-- venv/
```

---
### What each file does
- migration: here Django store some files to keep track of the changes you create in the models.py file, so to keep the database and the models.py synchronized.
- admin.py: this is a configuration file for a built-in Django app called Django Admin.
- apps.py: this is a configuration file of the app itself.
- models.py: here is where we define the entities of our Web application. The models are translated automatically by Django into database tables. 
- tests.py: this file is used to write unit tests for the app.
- views.py: this is the file where we handle the request/response cycle of our Web application.


---
### First view
Let’s write our first view. We will explore it in great detail in the next tutorial. 

But for now, let’s just experiment how it looks like to create a new page with Django

Open the views.py file inside the boards app, and add the following code:
```
from django.http import HttpResponse
def home(request):
    return HttpResponse('Hello, World!')
```

So, here we defined a simple view called home which simply returns a message saying Hello, World!

---
### First url mapping 
Now we have to tell Django when to serve this view. It’s done inside the urls.py file:
```
from django.conf.urls import url 
from django.contrib import admin
from boards import views

urlpatterns = [
    url(r'^$', views.home, name='home'), 
    url(r'^admin/', admin.site.urls), 
]
```

---
### Run and test
Run the server
```
python manage.py runserver
```

Test in a Web browser, open the http://127.0.0.1:8000 


---
# CONGRATS!!

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Making the first page

---
<!-- .slide: data-background="url('images/lab2.jpg')" data-background-size="cover"  --> 
<!-- .slide: class="lab" -->
## Lab time!
Making your first page



