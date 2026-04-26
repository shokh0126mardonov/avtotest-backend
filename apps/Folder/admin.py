from django.contrib import admin

from .models import Folder, MediaFile

admin.site.register([Folder, MediaFile])
