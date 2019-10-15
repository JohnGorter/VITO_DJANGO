# Static Files

---
### Static Files

Static files are
- CSS
- JavaScripts
- Fonts
- Images
- any other resources

DJANGO does not serve the files automatically

---
### Static files
Django provides some features to help us manage the static files
- django.contrib.staticfiles application 
- INSTALLED_APPS configuration

Setup
- create a static map for the static files
- add this directory to the settings
- use the {% load static %} template tag 
- refer to the {% static % resources

---
### Create a map

This is the easy part. At the root of the project
create a folder and copy and paste the files into them.

---
### Add static folder to settings

Change the settings.py to contain the static url
```
STATIC_URL = "/static/"
STATICFILES_DIR = [
  os.path.join(BASE_DIR, 'static')
]
```

---
### Load and use the static files
Change the template to use the static files
```
{% load static %}<!DOCTYPE html> <html>
<head>
<meta charset="utf-8">
<title>Boards</title>
<link rel="stylesheet" href="{% static 'css/bootstrap.
</head> <body>
<!-- body suppressed for brevity ... --> </body>
</html>

```
---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Using static files


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Style your application