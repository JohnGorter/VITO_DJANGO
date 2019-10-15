# More Templates

---
### More Templates

Templates can be 
- reusable 
- create a master page and only adding the unique part for each template


---
### Example reusable template

templates/base.html
```
{% load static %}<!DOCTYPE html> <html>
<head>
<meta charset="utf-8">
<title>{% block title %}Django Boards{% endblock
<link rel="stylesheet" href="{% static 'css/bootstrap.
</head> <body>
/articles/2016/01/ Captures{'year': '2016', 'month': '01'}
      m
<div class="container">
<ol class="breadcrumb my-4">
{% block breadcrumb %}
{% endblock %} </ol>
{% block content %}
{% endblock %} </div>
</body> </html>
```

---
### Example reusable template (2)

To use the template, extend from it
```
{% extends 'base.html' %}
{% block breadcrumb %}
<li class="breadcrumb-item active">Boards</li>
{% endblock %}
{% block content %} <table class="table">
<thead class="thead-inverse"> <tr>
<th>Board</th> <th>Posts</th> <th>Topics</th> <th>Last Post</th>
</tr> </thead>
<tbody>
{% for board in boards %}
<tr> <td>
<a href="{% url 'board_topics' board.pk %}
<small class="text-muted d-block">{{ board.des </td>
<td class="align-middle">0</td> <td class="align-middle">0</td> <td></td>
</tr>
{% endfor %}
</tbody> </table>
{% endblock %}
```

---
### Include
You can include html using

```

....
{% include 'includes/SOMETHING.html' %}
...
{% endblock %}
```

This allows you to include snippets of reusable HTML

---

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Setting up reuseable templates


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Writing your reusable templates
