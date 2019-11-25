# Swagger

---
### What Is OpenAPI?
OpenAPI Specification (formerly Swagger Specification) is an API description format for REST APIs

An OpenAPI file allows you to describe your entire API, including:
- Available endpoints and operations 
- Operation parameters Input and output for each operation
- Authentication methods
- Contact information, license, terms of use and other information

---
### Format of OpenAPI?
API specifications can be written in YAML or JSON

The format is easy to learn and readable to both humans and machines

The complete OpenAPI Specification can be found on GitHub: OpenAPI 3.0 Specification

---
### What Is Swagger?
Swagger is a set of open-source tools built around the OpenAPI Specification that can help
- design
- build
- document
- consume REST APIs

Major Swagger tools include:
- Swagger Editor – browser-based editor where you can write OpenAPI specs
- Swagger UI – renders OpenAPI specs as interactive API documentation
- Swagger Codegen – generates server stubs and client libraries from an OpenAPI spec

---
### Why Use OpenAPI?
The ability of APIs to describe their own structure is the root of all awesomeness in OpenAPI 

Once written, an OpenAPI specification and Swagger tools can drive your API development further in:
- Design-first users: use Swagger Codegen to generate a server stub for your API
- Use Swagger Codegen to generate client libraries for your API in over 40 languages
- Use Swagger UI to generate interactive API documentation that lets your users try out the API calls 
- Use the spec to connect API-related tools to your API

And more! 

---
### Documenting your API
REST framework provides built-in support for generating OpenAPI schemas, which can be used with tools that allow you to build API documentation

---
### Steps to inplement SWAGGERUI

Install additional packages
- install pyyaml
- install uritemplate

Add url paths
- path('openapi', get_schema_view(...), name='openapi-schema'),
- path('swagger-ui/', TemplateView.as_view(...), name='swagger-ui'),

Add template location to settings
- 'DIRS': [BASE_DIR + '/templates/',],

Add template file
- HTML file containing swagger ui markup


---
### Swagger UI Example
The HTML template for Swagger UI might be this:
```
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
        url: "{% url schema_url %}",
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      })
    </script>
  </body>
</html>
```

Save this in your templates folder as swagger-ui.html then route a TemplateView in your project's URL conf:
```
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
DRF SwaggerUI Demo

---
### Generate Swagger in DRF

There are also a number of great third-party documentation packages available.
Two popular options are 
- Swagger UI 
- ReDoc

Both require little more than the location of your static schema file or dynamic SchemaView endpoint

There are two popular Swagger UI generation packages
- django-rest-swagger (deprecated)
- drf-yasg

---
### Django REST Swagger installation
Installation
```
$ pip install django-rest-swagger
```

---
### Django REST Swagger configuration
Add 'rest_framework_swagger' to INSTALLED_APPS in Django settings.
```
INSTALLED_APPS = [
    ...
    'rest_framework_swagger',
    ...
]
```

---
### Django REST Swagger usage

To quickly get started, use the get_swagger_view shortcut. This will produce a schema view which uses common settings

Example
```
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Movie API')

urlpatterns = [
    path("swagger_ui/", schema_view)
]
```

---
### Django REST Extra Setup

Because the rest_framework_swagger framework uses the older schema generation API, we still need to set
```
REST_FRAMEWORK = {
...
'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
DRF Swagger Framework


---
### DRF-YASG

Features
- full support for nested Serializers and Schemas
- response schemas and descriptions
- model definitions compatible with codegen tools
- customization hooks at all points in the spec generation process
- JSON and YAML format for spec
- bundles latest version of swagger-ui and redoc for viewing the generated documentation
- schema view is cacheable out of the box
- generated Swagger schema can be automatically validated by swagger-spec-validator or flex

---
### DRF-YASG Usage

Installation
```
pip install drf-yasg
pip install swagger-spec-validator
```


---
### DRF-YASG Quickstart
To expose 4 cached, validated and publicly available endpoints:

- A JSON view of your API specification at /swagger.json
- A YAML view of your API specification at /swagger.yaml
- A swagger-ui view of your API specification at /swagger/
- A ReDoc view of your API specification at /redoc/

You need to use the following configuration...

---
### DRF-YASG Quickstart (2)
In settings.py:
```
INSTALLED_APPS = [
   ...
   'drf_yasg',
   ...
]
```
In urls.py:
```
...
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
...
schema_view = get_schema_view(
   openapi.Info(
      title="Movies API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['ssv', 'flex'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   re_path(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
   ...
]
```

---
### DRF-YASG Configuration

Lots and lots of configuration settings, for example:
```
SWAGGER_SETTINGS = {
   # default inspector classes, see advanced documentation
   'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
   'DEFAULT_FIELD_INSPECTORS': [
      'drf_yasg.inspectors.CamelCaseJSONFilter',
      'drf_yasg.inspectors.ReferencingSerializerInspector',
      'drf_yasg.inspectors.RelatedFieldInspector',
      'drf_yasg.inspectors.ChoiceFieldInspector',
      'drf_yasg.inspectors.FileFieldInspector',
      'drf_yasg.inspectors.DictFieldInspector',
      'drf_yasg.inspectors.SimpleFieldInspector',
      'drf_yasg.inspectors.StringDefaultFieldInspector',
   ],
   'DEFAULT_FILTER_INSPECTORS': [
      'drf_yasg.inspectors.CoreAPICompatInspector',
   ],
   'DEFAULT_PAGINATOR_INSPECTORS': [
      'drf_yasg.inspectors.DjangoRestResponsePagination',
      'drf_yasg.inspectors.CoreAPICompatInspector',
   ],

   # default api Info if none is otherwise given; should be an import string to an openapi.Info object
   'DEFAULT_INFO': None,
   # default API url if none is otherwise given
   'DEFAULT_API_URL': '',

   'USE_SESSION_AUTH': True,  # add Django Login and Django Logout buttons, CSRF token to swagger UI page
   'LOGIN_URL': getattr(django.conf.settings, 'LOGIN_URL', None),  # URL for the login button
   'LOGOUT_URL': getattr(django.conf.settings, 'LOGOUT_URL', None),  # URL for the logout button

   # Swagger security definitions to include in the schema;
   # see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object
   'SECURITY_DEFINITIONS': {
      'basic': {
         'type': 'basic'
      }
   },

   # url to an external Swagger validation service; defaults to 'http://online.swagger.io/validator/'
   # set to None to disable the schema validation badge in the UI
   'VALIDATOR_URL': '',

   # swagger-ui configuration settings, see https://github.com/swagger-api/swagger-ui/blob/112bca906553a937ac67adc2e500bdeed96d067b/docs/usage/configuration.md#parameters
   'OPERATIONS_SORTER': None,
   'TAGS_SORTER': None,
   'DOC_EXPANSION': 'list',
   'DEEP_LINKING': False,
   'SHOW_EXTENSIONS': True,
   'DEFAULT_MODEL_RENDERING': 'model',
   'DEFAULT_MODEL_DEPTH': 3,
}
REDOC_SETTINGS = {
   # ReDoc UI configuration settings, see https://github.com/Rebilly/ReDoc#redoc-tag-attributes
   'LAZY_RENDERING': True,
   'HIDE_HOSTNAME': False,
   'EXPAND_RESPONSES': 'all',
   'PATH_IN_MIDDLE': False,
}
```

---
### DRF-YASG Caching
Since the schema does not usually change during the lifetime of the django process
there is out of the box support for caching the schema view in-memory, with some sane defaults


---
### DRF-YASG Validation
Given the numerous methods to manually customize the generated schema, it makes sense to validate the result to ensure it still conforms to OpenAPI 2.0

To this end, validation is provided at the generation point using python swagger libraries
- can be activated by passing validators=[‘ssv’, ‘flex’] to get_schema_view 

if the generated schema is not valid, a SwaggerValidationError is raised by the handling codec.

Warning: This internal validation can slow down your server. Caching can mitigate the speed impact of validation.


The provided validation will catch syntactic errors, but more subtle violations of the spec might slip by them. To ensure compatibility with code generation tools, it is recommended to also employ one or more of the following methods:

---
### DRF-YASG swagger-ui validation badge

Online
- If your schema is publicly accessible, swagger-ui will automatically validate it against the official swagger online validator and display the result in the bottom-right validation badge.

Offline
- If your schema is not accessible from the internet, you can run a local copy of swagger-validator and set the VALIDATOR_URL accordingly:

```
SWAGGER_SETTINGS = {
    ...
    'VALIDATOR_URL': 'http://localhost:8189',
    ...
}
```

---
### Swagger in Django Rest Framework
Since Django Rest 3.7, there is now built in support for automatic OpenAPI 2.0 schema generation. However, this generation is based on the coreapi standard, which for the moment is vastly inferior to OpenAPI in both features and tooling support. In particular, the OpenAPI codec/compatibility layer provided has a few major problems:

- there is no support for documenting response schemas and status codes
- nested schemas do not work properly
- does not handle more complex fields such as FileField, ChoiceField, …

In short this makes the generated schema unusable for code generation, and mediocre at best for documentation.


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
DRF YASG Framework

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Generating Swagger documentation for your API