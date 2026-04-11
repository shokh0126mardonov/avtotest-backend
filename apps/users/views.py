from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializers,UserCreateSerializers,GetByUsername,UserSetPasswordSerializers

User = get_user_model()


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status



class UserApiViewSets(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializers
        return UserSerializers
    

class UserApiView(APIView):
    def get(self,request:Request)->Response:
        serializer = GetByUsername(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User,username = username)

        return Response(UserSerializers(user).data)
    
    def put(self,request:Request)->Request:
        serializers = UserSetPasswordSerializers(data = request.data)
        serializers.is_valid(raise_exception=True)

        password = serializers.get('password')
        serializers.update(request.user,password)






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