# Admin

---
### Admin

DJANGO has a built in admin site (app)
- listed in INSTALLED_APPS
- accessible through /admin
- python manage.py createsuperuser
- has Users and Groups



---
### Custom Models registration

You can register your models in the admin section:

- open the admin.py file in the boards directory
- add the following code:

boards/admin.py
```
from django.contrib import admin from .models import Board
admin.site.register(Board)
```
Save the admin.py file

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Exploring the admin section


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Exploring the admin section
