from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import AdminPermissions,InstructorPermissions
from apps.users.serializers import UserSerializers
from apps.Group.models import Group
from .serializers import UserGroupSerializers,GroupIdSerializers,GroupUserSerializers,SubmitAnswerSerializers,ExamSerializers
from .models import Exam

User = get_user_model()

class UserGroupViews(APIView):
    permission_classes = [IsAuthenticated,(AdminPermissions | InstructorPermissions)]


    def get(self, request:Request):
        serializer = GroupIdSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        group_id = data['group_id']

        group = get_object_or_404(Group,pk=group_id)

        return Response(GroupUserSerializers(group).data,200)
    
    def post(self, request:Request):
        serializer = UserGroupSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user_id = data['user_id']
        group_id = data['group_id']

        user = get_object_or_404(User,pk=user_id,role = 'student')
        group = get_object_or_404(Group,pk=group_id)

        group.users.add(user)

        return Response({"message": f"User {group.name} ga qo‘shildi"},201,content_type='json')
        

    def delete(self, request:Request):
        serializer = UserGroupSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user_id = data['user_id']
        group_id = data['group_id']

        user = get_object_or_404(User,pk=user_id)
        group = get_object_or_404(Group,pk=group_id)

        group.users.remove(user)

        return Response({"message": f"User {group.name} dan o'chirildi"},204,content_type='json')
    

class GroupInstructor(APIView):
    permission_classes = [IsAuthenticated,AdminPermissions]

    def get(self, request:Request):
        serializer = GroupIdSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data['group_id']

        group = get_object_or_404(Group,pk = group_id)

        return Response(UserSerializers(group.instructor).data)
    
class SubmitAnswerViews(APIView):

    def post(self,request:Request)->Response:
        serializers = SubmitAnswerSerializers(data = request.data)
        serializers.is_valid(raise_exception=True)
        data = serializers.save()
        return Response(ExamSerializers(data).data)


class GetExamApiView(APIView):
    def get(self,request:Request,pk)->Response:
        exam = get_object_or_404(Exam,pk = pk)
        return Response(ExamSerializers(exam).data)

class CheckExamApiview(APIView):
    def get(self,request:Request,pk)->Response:
        exam = get_object_or_404(Exam,pk = pk)
        return Response(ExamSerializers(exam).data)