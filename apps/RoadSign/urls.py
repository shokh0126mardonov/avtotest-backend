from django.urls import path

from .views import RoadSignFolderViewsets,RoadSignViewsets


urlpatterns = [
    path('',RoadSignViewsets.as_view({'get':'list',"post":"create"})),
    path('<int:pk>/',RoadSignViewsets.as_view({'get':'retrieve',"delete":"destroy",'put':"partial_update"})),

    path('folder/',RoadSignFolderViewsets.as_view({'get':'list',"post":"create"})),
    path('folder/',RoadSignFolderViewsets.as_view({'get':'retrieve',"delete":"destroy",'put':"partial_update"})),

]
