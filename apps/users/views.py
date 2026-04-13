from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializers,UserCreateSerializers,GetByUsername,UserSetPasswordSerializers
from .permissions import AdminPermissions,StudentPermissions,InstructorPermissions
User = get_user_model()


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status



class UserApiViewSets(ModelViewSet):
    queryset = User.objects.all()
    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve','destroy']:
            permission_classes = [IsAuthenticated, AdminPermissions]
        else:
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializers
        return UserSerializers
    


class UserApiView(ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'username':
            return GetByUsername
        elif self.action == 'password':
            return UserSetPasswordSerializers
    
    def get_permissions(self):
        if self.action == 'username':
            permission_classes =  [IsAuthenticated,AdminPermissions]
        elif self.action == 'password':
            permission_classes =  [IsAuthenticated]
        return [permission() for permission in permission_classes]

        

    @action(methods=['get'],url_name='get-username',detail=True)
    def username(self,request:Request)->Response:
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User,username = username)

        return Response(UserSerializers(user).data)
    
    def password(self,request:Request)->Response:
        serializer = self.get_serializer(instance=request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok dabba')
    


class LoginUser(TokenObtainPairView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user  

        if not user.is_active:
            return Response(
                {"detail": "User is not active"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
            'id': user.id
        })