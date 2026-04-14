from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.permissions import AdminPermissions
from .models import TestAnswer,TestCase
from .serializers import TestCaseSerializers

class TestCaseViewSets(ModelViewSet):
    permission_classes = [IsAuthenticated,AdminPermissions]
    authentication_classes = [JWTAuthentication]
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializers
