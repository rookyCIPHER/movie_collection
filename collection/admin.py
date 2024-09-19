from django.contrib import admin
from .models import Collection,MoviesInCollection
# Register your models here.

admin.site.register(Collection)
admin.site.register(MoviesInCollection)
