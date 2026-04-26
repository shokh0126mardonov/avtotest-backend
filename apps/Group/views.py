from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.permissions import AdminPermissions

from .models import Group
from .serializers import GroupSerializers


class GroupViewSets(ModelViewSet):
    queryset = Group.objects.filter(is_active=True).all()
    serializer_class = GroupSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, AdminPermissions]

        return [permission() for permission in permission_classes]
