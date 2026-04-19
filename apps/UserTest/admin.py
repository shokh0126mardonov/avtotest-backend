from django.contrib import admin

from .models import ExamTestCase,Exam

admin.site.register([Exam,ExamTestCase])