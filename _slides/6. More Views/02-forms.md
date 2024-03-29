# Forms

---
### Forms

To implement forms, there are two ways:
- the not so good way
- the better way

---
### Not so good

We could just create an html form:
templates/new_topic.html
```
{% extends 'base.html' %}
{% block title %}Start a New Topic{% endblock %}
{% block breadcrumb %}
<li class="breadcrumb-item"><a href="{% url 'home'
<li class="breadcrumb-item"><a href="{% url 'board_topic <li class="breadcrumb-item active">New topic</li>
{% endblock %}
{% block content %} <form method="post">
{% csrf_token %}
<div class="form-group">
<label for="id_subject">Subject</label>
<input type="text" class="form-control" id="id_subje </div>
<div class="form-group">
<label for="id_message">Message</label>
<textarea class="form-control" id="id_message" </div>
<button type="submit" class="btn btn-success">Post </form>
{% endblock %}

```

---
### Not so good (2)

The process would involve something like
```
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_ from .models import Board, Topic, Post
def new_topic(request, pk):
  board = get_object_or_404(Board, pk=pk)
  if request.method == 'POST':
    subject = request.POST['subject'] 
    message = request.POST['message']
    user = User.objects.first() # TODO: get the curre
    topic = Topic.objects.create( subject=subject,board=board, starter=user )
    post = Post.objects.create( message=message, topic=topic, created_by=user )
    return redirect('board_topics', pk=board.pk) 
  return render(request, 'new_topic.html', {'board'...
```

Wrongs:
- only considering the happy path 
- no  validation of  data


---
### The better way
use the Forms API
- available in the module django.forms

Django works with two types of forms: 
- forms.Form: a general purpose form implementation
- forms.ModelForm: a subclass of Form, and it’s associated with a model class


---
### The Forms base class (1)

this
```
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
```


renders...

```
<label for="your_name">Your name: </label>
<input id="your_name" type="text" name="your_name" maxlength="100" required>
```


---
### The Forms base class (2)

You could process the form in the view like 
```
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
```


---
### The Forms base class (3)

the template could be written as
```
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```

---
### More Forms

All form classes are created as subclasses of either 
- django.forms.Form 
- django.forms.ModelForm 

ModelForm is a subclass of Form
Form and ModelForm actually inherit common functionality from a (private) BaseForm class


---
### Model Forms (1)

boards/forms.py
```
from django import forms 
from .models import Topic

class NewTopicForm(forms.ModelForm):
  message = forms.CharField(widget=forms.Textarea(),
  class Meta:
    model = Topic
    fields = ['subject', 'message']
```

---
### Model Forms (2)

To handle the request
```
boards/views.py
-
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_ 
from .forms import NewTopicForm
from .models import Board, Topic, Post

def new_topic(request, pk):
  board = get_object_or_404(Board, pk=pk)
  user = User.objects.first() # TODO: get the currently 
  if request.method == 'POST':
    form = NewTopicForm(request.POST) 
    if form.is_valid():
      topic = form.save(commit=False) topic.board = board topic.starter = user topic.save()
      post = Post.objects.create( message=form.cleaned_data.get('message' topic=topic,created_by=user)
      return redirect('board_topics', pk=board.
    else:
      form = NewTopicForm()
  return render(request, 'new_topic.html', {'board'
```

---
### Model Forms (3)

The HTML

templates/new_topic.html
```
{% extends 'base.html' %}
{% block title %}Start a New Topic{% endblock %}
{% block breadcrumb %}
<li class="breadcrumb-item"><a href="{% url 'home'
<li class="breadcrumb-item"><a href="{% url 'board_topic <li class="breadcrumb-item active">New topic</li>
{% endblock %}
{% block content %} <form method="post">
{% csrf_token %}
{{ form.as_p }}
<button type="submit" class="btn btn-success">Post
</form>
{% endblock %}
```

Note the form.as_p here

---
### Model Forms (4)

The form have three rendering options: 
- form.as_table
- form.as_ul
- form.as_p 

It’s a quick way to render all the fields of a form

- create a static map for the static files
- add this directory to the settings
- use the {% load static %} template tag 
- refer to the {% static % resources


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Creating forms


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Creating Forms