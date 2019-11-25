# Security

---
### Security

Security consists of 
- authentication: who is making the request
- authorisation: what is allowed to be done

The ordering does matter

---
### Authentication (1)

Authentication is the mechanism of associating an incoming request with a set of identifying credentials, such as the user the request came from, or the token that it was signed with

---
### Authentication (2)

Authentication schemes are defined as a list of classes

DRF will attempt to authenticate with each class in the list 
- request.user and request.auth will be set using the return value of the first class that successfully authenticates

If no class authenticates
- request.user will be set to an instance of django.contrib.auth.models.AnonymousUser
- request.auth will be set to None.

Note: the value of request.user and request.auth for unauthenticated requests can be modified using the UNAUTHENTICATED_USER and UNAUTHENTICATED_TOKEN settings

---
### Authentication (3)

The default authentication schemes may be set globally
- DEFAULT_AUTHENTICATION_CLASSES setting

example
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

---
### Authentication (4)
The authentication scheme can be set on a per-view or per-viewset basis
```
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
```


---
### Authentication (5)

using the @api_view decorator with function based views.
```
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
```
---
### BasicAuthentication
This authentication scheme uses HTTP Basic Authentication
- generally only appropriate for testing

If successfully authenticated, BasicAuthentication provides 
- request.user will be a Django User instance
- request.auth will be None


Note: If you use BasicAuthentication
- ensure that your API is only available over https
- ensure API clients will always re-request the username and password at login


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
BasicAuthentication

---
### TokenAuthentication (1)
This authentication scheme uses a simple token-based HTTP Authentication scheme

Token authentication is appropriate for 
- client-server setups such as native desktop and mobile clients

To use, configure the authentication classes to include TokenAuthentication, 
and include rest_framework.authtoken in your INSTALLED_APPS setting
```
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

Note: Make sure to run manage.py migrate after changing your settings
The rest_framework.authtoken app provides Django database migrations

---
### TokenAuthentication (2)
To create tokens your clients can use
```
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

For clients to authenticate, the token key should be included in the Authorization HTTP header
- key should be prefixed by the string literal "Token", with whitespace separating the two strings

---
### TokenAuthentication example

example
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Note: If you want to use a different keyword in the header, such as Bearer, simply subclass TokenAuthentication and set the keyword class variable

---
### TokenAuthentication 
If successfully authenticated, TokenAuthentication provides the following credentials.
- request.user will be a Django User instance.
- request.auth will be a rest_framework.authtoken.models.Token instance

Unauthenticated responses that are denied permission will result in an HTTP 401 Unauthorized response with an appropriate WWW-Authenticate header

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
TokenAuthentication

---
### Generating Tokens
Tokens can be generated automatically
- by using signals
- by exposing an api endpoint
- with Django Admin
- using Django manage.py command

---
### Generating Tokens using signals
If you want every user to have an automatically generated Token, simply catch the User's post_save signal
```
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

If you've already created some users, you can generate tokens for all existing users like this:
```
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

---
### Generating Tokens using api endpoint
When using TokenAuthentication, you may want to provide a mechanism for clients to obtain a token given the username and password

DRF provides a built-in view to provide this behavior
- add the obtain_auth_token view to your URLconf

```
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]
```

The obtain_auth_token view will return a JSON response when valid username and password fields are POSTed to the view using form data or JSON:
```
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Note that the default obtain_auth_token view explicitly uses JSON requests and responses, rather than using default renderer and parser classes in your settings.

---
### Generating Tokens using custom View

If you need a customized version of the obtain_auth_token view
- subclass the ObtainAuthToken view class

For example, you may return additional user information beyond the token value:
```
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
```

---
### Generating Tokens using custom View (2)
And in your urls.py
```
urlpatterns += [
    url(r'^api-token-auth/', CustomAuthToken.as_view())
]
```

---
### Generating Tokens with Django admin
It is also possible to create Tokens manually through admin interface

movies/admin.py
```
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Creating tokens using Django Admin

---
### Generating Tokens using Django manage.py command
Since version 3.6.4 it's possible to generate a user token using the following command:
```
./manage.py drf_create_token <username>
```

this command will return the API token for the given user, creating it if it doesn't exist
```
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

In case you want to regenerate the token (for example if it has been compromised or leaked) you can pass an additional parameter:
```
./manage.py drf_create_token -r <username>
```

---
### SessionAuthentication
This authentication scheme uses Django's default session backend for authentication
- appropriate for AJAX clients that are running in the same session context as your website

If successfully authenticated, SessionAuthentication provides the following credentials.
- request.user will be a Django User instance
- request.auth will be None

Unauthenticated responses that are denied permission will result in an HTTP 403 Forbidden response

---
### Custom authentication
To implement a custom authentication scheme
- subclass BaseAuthentication 
- override the .authenticate(self, request) method

The method should return a two-tuple of (user, auth) if authentication succeeds, or None otherwise

---
### Custom authentication (2)

Typically the approach you should take is:
- if authentication is not attempted, return None, any other authentication schemes also in use will still be checked.
- if authentication is attempted but fails, raise a AuthenticationFailed exception
- you may also override the .authenticate_header(self, request) method 
    - it should return a string that will be used as the value of the WWW-Authenticate header in a HTTP 401 Unauthorized response



---
### Custom authentication example
The following example will authenticate any incoming request as the user given by the username in a custom request header named 'X-USERNAME'
```
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
```

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
Custom Authentication

---
### JSON Web Token Authentication
JSON Web Token is a fairly new standard which can be used for token-based authentication

JWT Authentication doesn't need to use a database to validate a token
package
- djangorestframework-simplejwt

---
### JSON Web Token Authentication setup
Installation
```
pip install djangorestframework_simplejwt
```

Then, in settings.py, add rest_framework_simplejwt.authentication.JWTAuthentication 
```
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
```


---
### JSON Web Token Authentication setup (2)

In your root urls.py file, include routes for Simple JWT's TokenObtainPairView and TokenRefreshView views:
```
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```

---
### JSON Web Token Authentication setup (3)

You can also include a route for Simple JWT's TokenVerifyView if you wish to allow API users to verify HMAC-signed tokens without having access to your signing key:
```
urlpatterns = [
    ...
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ...
]
```

---
### JSON Web Token Authentication usage
To verify that Simple JWT is working, you can use curl to issue a couple of test requests:
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "johngorter", "password": "john"}' \
  http://localhost:8000/api/token/

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```


---
### JSON Web Token Authentication usage (2)
You can use the returned access token to prove authentication for a protected view:
```
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```


---
### JSON Web Token Authentication usage(3)
When this short-lived access token expires, you can use the longer-lived refresh token to obtain another access token:
```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNTY3LCJqdGkiOiJjNzE4ZTVkNjgzZWQ0NTQyYTU0NWJkM2VmMGI0ZGQ0ZSJ9.ekxRxgb9OKmHkfy-zs1Ro_xs1eMLXiR17dIDBVxeT-w"}
```

---
### JSON Web Token Authentication settings
Some of Simple JWT's behavior can be customized through settings variables in settings.py:

```
from datetime import timedelta

...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

Above, the default values for these settings are shown

---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Demo time!
JWT Authentication


---
<!-- .slide: data-background="url('images/demo.jpg')" data-background-size="cover" --> 
<!-- .slide: class="lab" -->
## Lab time!
Implementing Authentication

