# Views

---
### Views

The UI of your website
- HttpResponse object returned from method

Steps to implement
- route an url to your method
- return an HttpResponse to the client

---
### Example
To route a url, change the urls.py

example:
```
from django.urls import path
from boards import views

urlpatterns = [
  path('',views.home, name="home")
  path('admin/', admin.site.urls)
]
```

---
### Example
To respond to a client, change the views.py

example:
```
from django.http import HttpResponse

def home(request):
  return HttpResponse('Hello World')

```

---
### Templates
Templates are html pages to use for in our methods
- HTML pages
- Placeholders with default content
- folder named 'templates'
- added through settings.py

---
### Templates setup
change the settings.py to:
```
TEMPLATES = [
  ...
  'DIRS':[os.path.join(BASE_DIR, 'templates')]
]
```

---
### Templates usage
To use the template, change the views.py

example:
```
from django.shortcuts import render

def home(request):
  return render(request, 'main.html', {'data':Hello World'})
```

---
### Template Syntax

Fragment of template:
```html
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Setting up templates


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Writing your templates
