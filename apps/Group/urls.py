from django.urls import path

from .views import GroupViewSets


urlpatterns = [
    path("", GroupViewSets.as_view({"get": "list", "post": "create"})),
    path(
        "<int:pk>/",
        GroupViewSets.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "partial_update"}
        ),
    ),
]
