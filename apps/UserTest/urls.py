from django.urls import path

from .views import UserGroupViews,GroupInstructor

urlpatterns = [
    path('StudentsToGroup/',UserGroupViews.as_view()),
    path('GetGroupInstructor/',GroupInstructor.as_view()),
]
