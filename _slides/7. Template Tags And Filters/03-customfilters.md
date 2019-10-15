# Custom Template tags 

---
### Custom Template tags 

Write your own template tag
- extend the template engine by defining custom tags
- make them available to your templates using the {% load %} tag

---
### Code layout
The most common place 
- inside a Django app: if they relate to an existing app, it makes sense to bundle them there

- any tags in the conventional location are automatically made available to load within templates
- app should contain a templatetags directory, at the same level as models.py, views.py, etc. 

If this doesn’t already exist, create it 
 - don’t forget the __init__.py file

After adding the templatetags module, you will need to restart your server before you can use the tags or filters in templates.

---
### Example

For example, if your custom tags/filters are in a file called poll_extras.py, your app layout might look like this:
```
polls/
    __init__.py
    models.py
    templatetags/
        __init__.py
        poll_extras.py
    views.py
```

in your template you would use the following:
```
{% load poll_extras %}
```
The app that contains the custom tags must be in INSTALLED_APPS in order for the {% load %} tag to work

---
### Example (2)
To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance, 

```
from django import template
register = template.Library()
```

Alternatively, template tag modules can be registered through the 'libraries' argument to DjangoTemplates


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Custom template tags


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Custom template tags

