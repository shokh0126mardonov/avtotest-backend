from django.urls import path

from .views import FolderViewSets, MediaViewSets

urlpatterns = [
    path("Folder/", FolderViewSets.as_view({"get": "list", "post": "create"})),
    path(
        "Folder/<int:pk>/",
        FolderViewSets.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "partial_update"}
        ),
    ),
    path("Media/", MediaViewSets.as_view({"get": "list", "post": "create"})),
    path(
        "Media/<int:pk>/",
        MediaViewSets.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "partial_update"}
        ),
    ),
]
