# Testing Views

---
### Testing Views

Views can be tested
- for their response codes
- for presence of content
- for syntax errors in python code (error 500)
- for url to view mapping

---
### Example of a test

```
from django.urls import reverse  
from django.test import TestCase

class HomeTests(TestCase):
  def test_home_view_status_code(self):
    url = reverse('home')
    response = self.client.get(url) 
    self.assertEquals(response.status_code, 200)

```

---
### Example of a test
boards/tests.py

```
from django.urls import reverse  
from django.test import TestCase
from .views import home

class HomeTests(TestCase):
  def test_home_view_status_code(self):
    url = reverse('home')
    response = self.client.get(url) 
    self.assertEquals(response.status_code, 200)

  def test_home_url_resolves_home_view(self): 
    view = resolve('/') 
    self.assertEquals(view.func, home)
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

tip: python manage.py test --verbosity=2

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
