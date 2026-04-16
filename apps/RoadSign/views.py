from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.permissions import AdminPermissions
from .models import RoadSign,RoadSignFolder
from .serializers import RoadSignFolderSerializer,RoadSignSerializer


class RoadSignViewsets(ModelViewSet):
    queryset = RoadSign.objects.all()
    serializer_class = RoadSignSerializer

    def get_permissions(self):
        if self.action == 'get':
            return [IsAuthenticated]
        return [IsAuthenticated,AdminPermissions]


class RoadSignFolderViewsets(ModelViewSet):
    queryset = RoadSignFolder.objects.all()
    serializer_class = RoadSignFolderSerializer

    def get_permissions(self):
        if self.action == 'get':
            return [IsAuthenticated]
        return [IsAuthenticated,AdminPermissions]