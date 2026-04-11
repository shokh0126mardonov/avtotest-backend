from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

from .views import UserApiViewSets,LoginUser,UserApiView

urlpatterns = [
    path('login/', LoginUser.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),


    path("",UserApiViewSets.as_view({'get':'list',"post":"create"})),
    path("<int:pk>/",UserApiViewSets.as_view({'get':'retrieve','delete':"destroy","patch":'partial_update'})),

    path('username/',UserApiView.as_view()),
    path('set-password/',UserApiView.as_view())


]

