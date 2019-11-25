from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import Movie
from guardian.admin import GuardedModelAdmin

TokenAdmin.raw_id_fields = ['user']


# Register your models here.
class MovieAdmin(GuardedModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(Movie, MovieAdmin)
