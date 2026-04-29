from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


from .serializers import (
    UserSerializers,
    UserCreateSerializers,
    GetByUsername,
    UserSetPasswordSerializers,
    LoginSerializers,
    LogoutSerializers,
)
from .permissions import AdminPermissions
from .models import DeviceLock

User = get_user_model()


class UserApiViewSets(ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ["list", "create", "retrieve", "destroy", "partial_update"]:
            permission_classes = [IsAuthenticated, AdminPermissions]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return UserCreateSerializers
        return UserSerializers


class UserApiView(ModelViewSet):
    def get_serializer_class(self):
        if self.action == "username":
            return GetByUsername
        elif self.action == "password":
            return UserSetPasswordSerializers

    def get_permissions(self):
        if self.action == "username":
            permission_classes = [IsAuthenticated, AdminPermissions]
        elif self.action == "password":
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=["get"], url_name="get-username", detail=True)
    def username(self, request: Request) -> Response:
        ids = list(User.objects.values_list("id", flat=True))
        print(ids)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        user = get_object_or_404(User, username=username)

        return Response(UserSerializers(user).data)

    def password(self, request: Request) -> Response:
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        device_id = serializer.validated_data.get("device_id")
        telegram_id = serializer.validated_data.get("telegram_id")
        user_agent = serializer.validated_data.get("user_agent")

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("Login yoki parol noto'g'ri")

        if not user.is_active:
            raise AuthenticationFailed("Foydalanuvchi aktiv emas")

        device = DeviceLock.objects.filter(user=user).first()

        if device is None:
            device = DeviceLock.objects.create(
                user=user,
                device_id=device_id,
                telegram_id=telegram_id,
                user_agent=user_agent,
            )

        if telegram_id:
            if device.telegram_id is None:
                device.telegram_id = telegram_id
                device.save(update_fields=["telegram_id"])
            elif device.telegram_id != telegram_id:
                return Response(
                {"error": "Siz boshqa telegramga ulangan qurilmadasiz"},
                status=403
            )

        if device_id:
            if device.device_id is None:
                device.device_id = device_id
                device.save(update_fields=["device_id"])
            elif device.device_id != device_id:
                return Response(
                    {"error": "Siz boshqa telegramga ulangan qurilmadasiz"},
                    status=403
                )

        token = RefreshToken.for_user(user)

        return Response(
            {
            "access": str(token.access_token),
            "refresh": str(token),
            "id":user.pk,
            "role":str(user.role)
            },
            status=200
        )


class LogoutViews(APIView):
    def post(self, request: Request) -> Response:
        serializer = LogoutSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        device_id = serializer.validated_data.get("device_id")
        telegram_id = serializer.validated_data.get("telegram_id")

        if telegram_id:
            device = DeviceLock.objects.filter(telegram_id=telegram_id).first()
            if device:
                device.telegram_id = None
                device.save()
                return Response(status=204)

            elif device is None:
                return Response("bu telegram id bazada mavjud emas!", status=400)

        elif device_id:
            device = DeviceLock.objects.filter(device_id=device_id).first()

            if device:
                device.device_id = None
                device.save()
                return Response(status=204)

            elif device is None:
                return Response("bu device id bazada mavjud emas!", status=400)
