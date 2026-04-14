from django.urls import path

from .views import TestCaseViewSets

urlpatterns = [
    path('',TestCaseViewSets.as_view({"get":"list",'post':'create'})),
    path('<int:pk>/',TestCaseViewSets.as_view({"get":"retrieve"})),

]
