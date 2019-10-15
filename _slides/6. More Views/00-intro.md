# More Views

---
### First: More URLS

Define URLS in an URLconf (URL configuration). 
- is a mapping between URL path expressions to Python functions (your views)

- this mapping can be as short or as long as needed. 
- it can reference other mappings
- it can be constructed dynamically

---
### How Django processes a request
A page request triggers the following algoritm
- Django determines the root URLconf module to use
    - ordinarily, this is the value of the ROOT_URLCONF setting
- Django loads looks for the variable urlpatterns
    - this should be a sequence of django.urls.path() and/or django.urls.re_path() instances
- Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL

Once one of the URL patterns matches: 
- Django imports and calls the given view, which is a simple Python function (or a class-based view)
- The view gets passed the following arguments:
    - An instance of HttpRequest
    - the matches from the regular expression are provided as positional arguments

If no URL pattern matches or if an exception is raised 
- Django invokes an appropriate error-handling view

---
### Example configuration
Here’s a sample URLconf:
```
from django.urls import path
from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
// There’s no need to add a leading slash, because every URL has that. For example, it’s articles, not /articles
```
Notes:
- To capture a value from the URL, use angle brackets
- Captured values can optionally include a converter type

There’s no need to add a leading slash, because every URL has that. For example, it’s articles, not /articles

---
### Example requests

- /articles/2005/03/ would match the third entry in the list
- /articles/2003/ would match the first pattern in the list, not the second one, because the patterns are tested in order
- /articles/2003 would not match any of these patterns, because each pattern requires that the URL end with a slash
- /articles/2003/03/building-a-django-site/ would match the final pattern

---
### Path converters
The following path converters are available by default:

- str 
    - matches any non-empty string, excluding the path separator, '/'  
    - the default if a converter isn’t included in the expression
- int 
    - matches zero or any positive integer
    - returns an int
- slug 
    - matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters
    - for example, building-your-1st-django-site.
- uuid 
    - matches a formatted UUID 
    - for example, 075194d3-6885-417e-a8a8-6c931e272f00
    - returns a UUID instance
- path 
    - matches any non-empty string, including the path separator, '/'
    - allows you to match against a complete URL path rather than just a segment of a URL path as with str

---
### Registering custom path converters
For more complex matching requirements, you can define your own path converters

A converter is a class that includes the following:
- a regex class attribute, as a string
- a to_python(self, value) method, which handles converting the matched string into the type that should be passed to the view function.
- a to_url(self, value) method, which handles converting the Python type into a string to be used in the URL

---
### Custom path converter example:
For example:
```
class FourDigitYearConverter:
    regex = '[0-9]{4}'
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return '%04d' % value
```

Register custom converter classes in your URLconf using register_converter():
```
from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')
urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<yyyy:year>/', views.year_archive),
    ...
]
```

---
### Using regular expressions
You can also use regular expressions using re_path() instead of path()

The syntax for named regular expression groups is 
- (?P<name>pattern), where name is the name of the group and pattern is some pattern to match

Here’s the example URLconf from earlier, rewritten using regular expressions:
```
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
```

This accomplishes roughly the same thing as the previous example, except
- exact URLs that will match are slightly more constrained
 - for example, the year 10000 will no longer match since the year integers are constrained to be exactly four digits long
 - each captured argument is sent to the view as a string, regardless of what sort of match the regular expression makes


---
### What the URLconf searches against
The URLconf searches against the requested URL, as a normal Python string

This does not include GET or POST parameters, or the domain name

For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/
In a request to https://www.example.com/myapp/?page=3, the URLconf will look for myapp/

The URLconf doesn’t look at the request method
- all request methods – POST, GET, HEAD, etc. will be routed to the same function for the same URL

---
### Specifying defaults for view arguments

A convenient trick is to specify default parameters for your views’ arguments. Here’s an example URLconf and view:
URLconf
```
from django.urls import path
from . import views
urlpatterns = [
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
]
```

View (in blog/views.py)
```
def page(request, num=1):
    # Output the appropriate page of blog entries, according to num.
    ...
```

In the above example, both URL patterns point to the same view 
– views.page 
– the first pattern doesn’t capture anything from the URL
- if the first pattern matches, the page() function will use its default argument for num, 1
- if the second pattern matches, page() will use whatever num value was captured

---
### Performance
Each regular expression in a urlpatterns is compiled the first time it’s accessed
This makes the system blazingly fast

- urlpatterns should be a sequence of path() and/or re_path() instances

---
### Error handling
When a match for the requested URL cant be found, or when an exception is raised
- Django invokes an error-handling view.

The views to use for these cases are specified by four variables.
Their default values should suffice for most projects, 
but further customization is possible by overriding their default values.

- values can be set in your root URLconf. 
- setting these variables in any other URLconf will have no effect
- values must be callables, or strings representing the full Python import path to the view 

---
### Error handling (2)
The variables are:

- handler400 – See django.conf.urls.handler400.
- handler403 – See django.conf.urls.handler403.
- handler404 – See django.conf.urls.handler404.
- handler500 – See django.conf.urls.handler500.

---
### Including other URLconfs
At any point, your urlpatterns can “include” other URLconf modules
- this essentially “roots” a set of URLs below other ones

For example
```
from django.urls import include, path

urlpatterns = [
    # ... snip ...
    path('community/', include('aggregator.urls')),
    path('contact/', include('contact.urls')),
    # ... snip ...
]
```

Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing

---
### Including other URLconfs (2)
Another possibility is to include additional URL patterns by using a list of path() instances

For example, consider this URLconf:
```
from django.urls import include, path
from apps.main import views as main_views
from credit import views as credit_views

extra_patterns = [
    path('reports/', credit_views.report),
    path('reports/<int:id>/', credit_views.report),
    path('charge/', credit_views.charge),
]

urlpatterns = [
    path('', main_views.homepage),
    path('help/', include('apps.help.urls')),
    path('credit/', include(extra_patterns)),
]
```

In this example, the /credit/reports/ URL will be handled by the credit_views.report() Django view

---
### Captured parameters
An included URLconf receives any captured parameters from parent URLconfs, so the following example is valid:

In settings/urls/main.py
```
from django.urls import include, path

urlpatterns = [
    path('<username>/blog/', include('foo.urls.blog')),
]
```

In foo/urls/blog.py
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog.index),
    path('archive/', views.blog.archive),
]
```

In the above example, the captured "username" variable is passed to the included URLconf, as expected

---
### Passing extra options to view functions
URLconfs have a hook that lets you pass extra arguments to your view functions, as a Python dictionary

The path() function can take an optional third argument

For example:
```
from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]
```

In this example, for a request to /blog/2005/, Django will call views.year_archive(request, year=2005, foo='bar')

---
### Dealing with conflicts

It’s possible to have a URL pattern which captures named keyword arguments, 
and also passes arguments with the same names in its dictionary of extra arguments
- the arguments in the dictionary will be used instead of the arguments captured in the URL

---
### Reverse resolution of URLs

It is strongly desirable to avoid hard-coding these URLs 
Equally dangerous is devising ad-hoc mechanisms to generate URLs that are parallel to the design described by the URLconf, which can result in the production of URLs that become stale over time

- The primary piece of information to get a URL is an identification (e.g. the name) of the view in charge of handling it
- Other pieces of information that necessarily must participate in the lookup of the right URL are the types (positional, keyword) and values of the view arguments

Django provides a solution such that the URL mapper is the only repository of the URL design
- You feed it with your URLconf and then it can be used in both directions

---
### Reverse resolution of URLs (2)

Django provides tools for performing URL reversing that match the different layers where URLs are needed:
- In templates: Using the url template tag
- In Python code: Using the reverse() function

In higher level code related to handling of URLs of Django model instances
- The get_absolute_url() method

---
### Reverse resolution of URLs (3)

Consider again this URLconf entry
```
from django.urls import path
from . import views

urlpatterns = [
    #...
    path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
    #...
]
```

---
### Reverse resolution of URLs (4)
According to this design, the URL for the archive corresponding to year nnnn is /articles/<nnnn>/.

You can obtain these in template code by using:
```
<a href="{% url 'news-year-archive' 2012 %}">2012 Archive</a>
{# Or with the year in a template context variable: #}
<ul>
{% for yearvar in year_list %}
<li><a href="{% url 'news-year-archive' yearvar %}">{{ yearvar }} Archive</a></li>
{% endfor %}
</ul>
```


---
### Reverse resolution of URLs (5)

Or in Python code:
```
from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect_to_year(request):
    # ...
    year = 2006
    # ...
    return HttpResponseRedirect(reverse('news-year-archive', args=(year,)))
```

If, for some reason, it was decided that the URLs where content for yearly article archives are published at should be changed then you would only need to change the entry in the URLconf


---
### Naming URL patterns
In order to perform URL reversing, you’ll need to use named URL patterns as done in the examples above
the string used for the URL name can contain any characters you like

- you are not restricted to valid Python names
- when naming URL patterns, choose names that are unlikely to clash with other applications’ choice of names
    - reverse() finds depends on whichever pattern is last in your project’s urlpatterns list
- put a prefix on your URL names, this decreases the chance of collision

You can deliberately choose the same URL name as another application if you want to override a view
- a common use case is to override the LoginView

You may also use the same name for multiple URL patterns if they differ in their arguments
- in addition to the URL name, reverse() matches the number of arguments and the names of the keyword arguments

---
### URL namespaces

URL namespaces allow you to uniquely reverse named URL patterns even if different applications use the same URL names

It’s a good practice for third-party apps to always use namespaced URLs (as we did in the tutorial)

Django applications that make proper use of URL namespacing can be deployed more than once for a particular site. 
- for example django.contrib.admin has an AdminSite class which allows you to easily deploy more than one instance of the admin


A URL namespace comes in two parts, both of which are strings:
- application namespace
    - describes the name of the application that is being deployed
- instance namespace
    - identifies a specific instance of an application
    - instance namespaces should be unique across your entire project


---
### URL namespaces (2)

Namespaced URLs are specified using the ':' operator

For example, the main index page of the admin application is referenced using 'admin:index'
- this indicates a namespace of 'admin', and a named URL of 'index'

Namespaces can also be nested
- the named URL 'sports:polls:index' would look for a pattern named 'index' in the namespace 'polls' that is itself defined within the top-level namespace 'sports'

---
### Reversing namespaced URLs
When given a namespaced URL (e.g. 'polls:index') to resolve:
- Django splits the fully qualified name into parts and then tries the following lookup:
    - first, Django looks for a matching application namespace
    - this will yield a list of instances of that application
    - if there is a current application defined, Django finds and returns the URL resolver for that instance. 
    - the current application can be specified with the current_app argument to the reverse() function

The url template tag uses the namespace of the currently resolved view as the current application in a RequestContext. You can override this default by setting the current application on the request.current_app attribute.

If there is no current application, Django looks for a default application instance. The default application instance is the instance that has an instance namespace matching the application namespace (in this example, an instance of polls called 'polls').

If there is no default application instance, Django will pick the last deployed instance of the application, whatever its instance name may be.

If the provided namespace doesn’t match an application namespace in step 1, Django will attempt a direct lookup of the namespace as an instance namespace.

If there are nested namespaces, these steps are repeated for each part of the namespace until only the view name is unresolved. The view name will then be resolved into a URL in the namespace that has been found.


---
### Example
To show this resolution strategy in action, consider an example of two instances of the polls application from the tutorial: 
- one called 'author-polls' 
- one called 'publisher-polls'

Assume we have enhanced that application so that it takes the instance namespace into consideration when creating and displaying polls

urls.py
```
from django.urls import include, path

urlpatterns = [
    path('author-polls/', include('polls.urls', namespace='author-polls')),
    path('publisher-polls/', include('polls.urls', namespace='publisher-polls')),
]
```
polls/urls.py
```
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ...
]
```

---
### Example (2)
Using this setup, the following lookups are possible:
- if one of the instances is current - say, if we were rendering the detail page in the instance 'author-polls' - 'polls:index' will resolve to the index page of the 'author-polls' instance; i.e. both of the following will result in "/author-polls/".

In the method of a class-based view:

reverse('polls:index', current_app=self.request.resolver_match.namespace)
and in the template:

{% url 'polls:index' %}
If there is no current instance - say, if we were rendering a page somewhere else on the site - 'polls:index' will resolve to the last registered instance of polls. Since there is no default instance (instance namespace of 'polls'), the last instance of polls that is registered will be used. This would be 'publisher-polls' since it’s declared last in the urlpatterns.

'author-polls:index' will always resolve to the index page of the instance 'author-polls' (and likewise for 'publisher-polls') .

If there were also a default instance - i.e., an instance named 'polls' - the only change from above would be in the case where there is no current instance (the second item in the list above). In this case 'polls:index' would resolve to the index page of the default instance instead of the instance declared last in urlpatterns.

URL namespaces and included URLconfs¶
Application namespaces of included URLconfs can be specified in two ways.

Firstly, you can set an app_name attribute in the included URLconf module, at the same level as the urlpatterns attribute. You have to pass the actual module, or a string reference to the module, to include(), not the list of urlpatterns itself.

polls/urls.py¶
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ...
]
urls.py¶
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
]
The URLs defined in polls.urls will have an application namespace polls.

Secondly, you can include an object that contains embedded namespace data. If you include() a list of path() or re_path() instances, the URLs contained in that object will be added to the global namespace. However, you can also include() a 2-tuple containing:

(<list of path()/re_path() instances>, <application namespace>)
For example:

from django.urls import include, path

from . import views

polls_patterns = ([
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
], 'polls')

urlpatterns = [
    path('polls/', include(polls_patterns)),
]
This will include the nominated URL patterns into the given application namespace.

The instance namespace can be specified using the namespace argument to include(). If the instance namespace is not specified, it will default to the included URLconf’s application namespace. This means it will also be the default instance for that namespace.



---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Advanced Urls


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Advanced Urls
