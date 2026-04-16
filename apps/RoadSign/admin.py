from django.contrib import admin

from .models import RoadSign,RoadSignFolder

admin.site.register([RoadSign,RoadSignFolder])