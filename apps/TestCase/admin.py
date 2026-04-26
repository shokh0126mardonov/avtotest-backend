from django.contrib import admin

from .models import TestAnswer, TestCase

admin.site.register([TestCase, TestAnswer])
