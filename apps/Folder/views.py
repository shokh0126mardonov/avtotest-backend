from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.permissions import AdminPermissions
from .models import MediaFile,Folder
from .serializers import FolderSerializers,MediaFileSerializers

class FolderViewSets(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializers
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated,AdminPermissions] 
        return [p() for p in permission_classes]
    
class MediaViewSets(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializers
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated,AdminPermissions] 
        return [p() for p in permission_classes]