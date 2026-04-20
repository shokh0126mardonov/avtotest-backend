from rest_framework import serializers

from apps.Group.models import Group
from apps.users.serializers import UserSerializers


class UserGroupSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(min_value = 1)
    group_id = serializers.IntegerField(min_value = 1)


class GroupIdSerializers(serializers.Serializer):
    group_id = serializers.IntegerField(min_value = 1)


class GroupUserSerializers(serializers.ModelSerializer):
    users = UserSerializers(read_only = True,many=True)
    class Meta:
        model = Group
        fields = ['pk','name','description','image','is_active','created_date','instructor','users']


# class ExamTestCaseSerializers(serializers.Serializer):
#     testCaseId = serializers.IntegerField(min_value = 1)
#     selectedAnswerId = serializers.IntegerField(min_value = 1)


class SubmitAnswerSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(min_value = 1)
    testCaseId = serializers.IntegerField(min_value = 1)
    selectedAnswerId = serializers.IntegerField(min_value = 1)