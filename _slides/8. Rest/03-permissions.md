# Permissions

---
### Permissions
Together with authentication and throttling, permissions determine whether a request should be granted or denied access

- permissions are a form of authorisation
- permission checks are always run at the very start of the view, before any other code is allowed to proceed
- permission checks will typically use the authentication information in the request.user and request.auth properties to determine if the incoming request should be permitted
- permissions are used to grant or deny access for different classes of users to different parts of the API

---
### Permissions (2)

The simplest style of permission id to allow access to any authenticated user, and deny access to any unauthenticated user
- corresponds to the IsAuthenticated class in REST framework

A slightly less strict style of permission is to allow full access to authenticated users, but allow read-only access to unauthenticated users
- corresponds to the IsAuthenticatedOrReadOnly class in REST framework

---
### How permissions are determined
Permissions in REST framework are always defined as a list of permission classes

- before running the main body of the view each permission in the list is checked 
- if any permission check fails an exceptions.PermissionDenied or exceptions.NotAuthenticated exception will be raised, and the main body of the view will not run

---
### How permissions fail
When the permissions checks fail either a "403 Forbidden" or a "401 Unauthorized" response will be returned, according to the following rules:
- the request was successfully authenticated, but permission was denied
    - an HTTP 403 Forbidden response will be returned
- the request was not successfully authenticated, and the highest priority authentication class does not use WWW-Authenticate headers. 
    - an HTTP 403 Forbidden response will be returned
- the request was not successfully authenticated, and the highest priority authentication class does use WWW-Authenticate headers
    - an HTTP 401 Unauthorized response, with an appropriate WWW-Authenticate header will be returned


---
### Object level permissions

Object level permissions are used to determine if a user should be allowed to act on a particular object
- typically be a model instance
- are run by REST framework's generic views when .get_object() is called

If you're writing your own views and want to enforce object level permissions
- call the .check_object_permissions(request, obj) method on the view at the point at which you've retrieved the object
    - this will either raise a PermissionDenied or NotAuthenticated exception, or simply return if the view has the appropriate permissions

---
### Object level permissions example 
example
```
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
```

Note: With the exception of DjangoObjectPermissions, the provided permission classes in rest_framework.permissions do not implement the methods necessary to check object permissions.

---
### Limitations of object level permissions
For performance reasons the generic views will not automatically apply object level permissions to each instance in a queryset when returning a list of objects

Often when you're using object level permissions you'll also want to filter the queryset appropriately, to ensure that users only have visibility onto instances that they are permitted to view.

---
### Setting the permission policy
The default permission policy may be set globally, using the DEFAULT_PERMISSION_CLASSES setting

For example
```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
If not specified, this setting defaults to allowing unrestricted access
```
'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
]
```

---
### View level permissions

You can also set the authentication policy on a 
- per-view 
- per-viewset 
basis, using the APIView class-based views

---
### View level permissions example 
example 
```
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

---
### View level permissions example (2)
Or, if you're using the @api_view decorator with function based views.
```
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

Note: when you set new permission classes through class attribute or decorators you're telling the view to ignore the default list set over the settings.py file

---
### Setting the permission policy
Provided they inherit from rest_framework.permissions.BasePermission
- permissions can be composed using standard Python bitwise operators

example, IsAuthenticatedOrReadOnly could be written:
```
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class ExampleView(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

Note: it supports & (and), | (or) and tilde (not).

---
### Permission classes 

|permission|description|
|---|---|
|AllowAny| allow unrestricted access|
|IsAuthenticated| deny permission to any unauthenticated user, and allow permission otherwise|
|IsAdminUser|deny permission to any user, unless user.is_staff is True|
|IsAuthenticatedOrReadOnly| allow authenticated users to perform any request|
|DjangoModelPermissions| granted if the user is authenticated and has the relevant model permissions assigned|
|DjangoModelPermissionsOrAnonReadOnly|Similar to DjangoModelPermissions, but also allows unauthenticated users to have read-only access to the API|
|DjangoObjectPermissions| allows per-object permissions on models|


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
IsAuthenticated permission

---
### Custom permissions
To implement a custom permission
- override BasePermission 
- implement either, or both, of the following methods:
    - .has_permission(self, request, view)
    - .has_object_permission(self, request, view, obj)

The methods should return True if the request should be granted access, and False otherwise


---
### Custom permissions example

The following is an example of a permission class that checks the incoming request's IP address against a blacklist, and denies the request if the IP has been blacklisted.

example global permission

```
from rest_framework import permissions

class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        return not blacklisted
```


---
### Custom permissions example

example object permission
```
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Custom permissions


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Implementing Permissions


---
### django-guardian 

an implementation of object permissions for Django providing an extra authentication backend
- integrates in admin backend

it features:
- object permissions for Django
- AnonymousUser support
- high level API
- heavily tested
- Django’s admin integration
- decorators

---
### django-guardion installation
to install
```
pip install django-guardian
```

---
### django-guardian configuration

add guardian to INSTALLED_APPS
```
INSTALLED_APPS = (
     ...
    'guardian',
)
```
hook guardian’s authentication backend:
```
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)
```
Once project is configured to work with django-guardian, calling migrate management command would create User instance for anonymous user support (with name of AnonymousUser).

The Guardian anonymous user is different from the Django Anonymous user. The Django Anonymous user does not have an entry in the database, however the Guardian anonymous user does.

---
### django-guardian usage

prepare permissions first
```
class Task(models.Model):
    summary = models.CharField(max_length=32)
    content = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('assign_task', 'Assign task'),  # custom permissions
        )
```

then call makemigrations and migrate
- our assign_task permission would be added to default set of permissions

---
### Assign object permissions for user
We can assign permissions for any user/group and object pairs using
- guardian.shortcuts.assign_perm()

For user
Continuing our example we now can allow Joe user to assign some task:
```
>>> from django.contrib.auth.models import User
>>> boss = User.objects.create(username='Big Boss')
>>> joe = User.objects.create(username='joe')
>>> task = Task.objects.create(summary='Some job', content='', reported_by=boss)
>>> from guardian.shortcuts import assign_perm
>>> assign_perm('assign_task', joe, task)
>>> joe.has_perm('assign_task', task)
True
```

---
### Assign object permissions for group

This case doesn’t really differ from user permissions assignment. The only difference is we have to pass Group instance rather than User.
```
>>> from django.contrib.auth.models import Group
>>> group = Group.objects.create(name='employees')
>>> assign_perm('change_task', group, task)
>>> joe.has_perm('change_task', task)
False
>>> # Well, joe is not yet within an *employees* group
>>> joe.groups.add(group)
>>> joe.has_perm('change_task', task)
True
```



---
### Assigning Permissions inside Signals

```
@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    user, created = kwargs["instance"], kwargs["created"]
    if created and user.username != settings.ANONYMOUS_USER_NAME:
        from profiles.models import Profile
        profile = Profile.objects.create(pk=user.pk, user=user, creator=user)
        assign_perm("change_user", user, user)
        assign_perm("change_profile", user, profile)
```
The check for user.username != settings.ANONYMOUS_USER_NAME is required otherwise the assign_perm calls will occur when the Anonymous User is created, however before there are any permissions available.

---
### Check object permissions
how about verifying permissions of a user or group
- the standard way
```
>>> joe.has_perm('sites.change_site')
False
```
And for a specific Site instance we do the same but we pass site as additional argument
```
>>> site = Site.objects.get_current()
>>> joe.has_perm('sites.change_site', site)
False
```

---
### Checking permissions inside views
Aside from the standard has_perm method, django-guardian provides some useful helpers for object permission checks

- get_perms: to check permissions we can use a quick-and-dirty shortcut
```
>>> from guardian.shortcuts import get_perms
>>>
>>> joe = User.objects.get(username='joe')
>>> site = Site.objects.get_current()
>>>
>>> 'change_site' in get_perms(joe, site)
True
```

---
### Checking permissions inside views (2)
- get_objects_for_user: extract list of objects based on particular user

```
from django.shortcuts import render
from django.template import RequestContext
from projects.models import Project
from guardian.shortcuts import get_objects_for_user

def user_dashboard(request, template_name='projects/dashboard.html'):
    projects = get_objects_for_user(request.user, 'projects.view_project')
    return render(request, template_name, {'projects': projects},
        RequestContext(request))
```

It is also possible to provide list of permissions rather than single string, own queryset (as klass argument) or control if result should be computed with (default) or without user’s groups permissions.

---
### ObjectPermissionChecker
At the core module of django-guardian, there is a guardian.core.ObjectPermissionChecker which checks permission of user/group for specific object

It caches results so it may be used at part of codes where we check permissions more than once

example
```
>>> joe = User.objects.get(username='joe')
>>> site = Site.objects.get_current()
>>> from guardian.core import ObjectPermissionChecker
>>> checker = ObjectPermissionChecker(joe) # we can pass user or group
>>> checker.has_perm('change_site', site)
True
>>> checker.has_perm('add_site', site) # no additional query made
False
>>> checker.get_perms(site)
[u'change_site']
```

---
### Using decorators
django-guardian is shipped with two decorators 
- permission_required
- permission_required_or_403 decorator

```
>>> joe = User.objects.get(username='joe')
>>> foobars = Group.objects.create(name='foobars')
>>>
>>> from guardian.decorators import permission_required_or_403
>>> from django.http import HttpResponse
>>>
>>> @permission_required_or_403('auth.change_group',
>>>     (Group, 'name', 'group_name'))
>>> def edit_group(request, group_name):
>>>     return HttpResponse('some form')
>>>
>>> from django.http import HttpRequest
>>> request = HttpRequest()
>>> request.user = joe
>>> edit_group(request, group_name='foobars')
<django.http.HttpResponseForbidden object at 0x102b43dd0>
>>>
>>> joe.groups.add(foobars)
>>> edit_group(request, group_name='foobars')
<django.http.HttpResponseForbidden object at 0x102b43e50>
>>>
>>> from guardian.shortcuts import assign_perm
>>> assign_perm('auth.change_group', joe, foobars)
<UserObjectPermission: foobars | joe | change_group>
>>>
>>> edit_group(request, group_name='foobars')
<django.http.HttpResponse object at 0x102b8c8d0>
>>> # Note that we now get normal HttpResponse, not forbidden
```

More on decorators can be read at corresponding API page.

---
### Inside templates
django-guardian comes with special template tag 
- guardian.templatetags.guardian_tags.get_obj_perms() 
```
{% load guardian_tags %}
...
{% get_obj_perms user/group for obj as "context_var" %}
```
Make sure that you set and use those permissions in same template block ({% block %})

example
```
{% get_obj_perms request.user for flatpage as "flatpage_perms" %}

{% if "delete_flatpage" in flatpage_perms %}
    <a href="/pages/delete?target={{ flatpage.url }}">Remove page</a>
{% endif %}
```

---
### Admin integration
Django comes with excellent and widely used Admin application
- it provides content management for Django applications
- user with access to admin panel can manage users, groups, permissions and other data provided by system.

use GuardedModelAdmin instead of django.contrib.admin.ModelAdmin for registering models within admin

```
from django.db import models

class Post(models.Model):
    title = models.CharField('title', max_length=64)
    slug = models.SlugField(max_length=64)
    content = models.TextField('content')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        permissions = (('hide_post', 'Can hide post'))
        get_latest_by = 'created_at'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return {'post_slug': self.slug}
```
---
### Admin integration (2)
We want to register Post model within admin application
```
from django.contrib import admin
from posts.models import Post
from guardian.admin import GuardedModelAdmin

class PostAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin.site.register(Post, PostAdmin)
```

We can now navigate to change post page and just next to the history link we can click Object permissions button to manage row level permissions

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Django guardian 


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Implement object level permissions using Django guardian

