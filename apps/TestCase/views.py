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

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     self.perform_create(serializer)

    #     return Response(
    #         {
    #             "message": "TestCase muvaffaqiyatli yaratildi",
    #             "data": serializer.data
    #         },
    #         status=status.HTTP_201_CREATED
    #     )