from django.urls import path

from .views import UserGroupViews,GroupInstructor,SubmitAnswerViews

urlpatterns = [
    path('StudentsToGroup/',UserGroupViews.as_view()),
    path('GetGroupInstructor/',GroupInstructor.as_view()),
    path('SubmitAnswers/',SubmitAnswerViews.as_view()),
]
