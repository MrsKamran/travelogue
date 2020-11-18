from django.contrib import admin
from .models import Posts, Reviews, Photo, DestinationMarker

# Register your models here.

admin.site.register(Posts)
admin.site.register(Reviews)
admin.site.register(Photo)
admin.site.register(DestinationMarker)
