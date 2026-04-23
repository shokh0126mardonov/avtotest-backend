from django.urls import path

from .views import UserGroupViews,GroupInstructor,SubmitAnswerViews,GetExamApiView,CheckExamApiview

urlpatterns = [
    path('StudentsToGroup/',UserGroupViews.as_view()),
    path('GetGroupInstructor/',GroupInstructor.as_view()),
    path('SubmitAnswers/',SubmitAnswerViews.as_view()),

    path('GetExams/<int:pk>/',GetExamApiView.as_view()),
    path('CheckExam/<int:pk>/',CheckExamApiview.as_view())

]
