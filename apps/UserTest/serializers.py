from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.TestCase.models import TestAnswer,TestCase
from apps.users.serializers import UserSerializers
from apps.Group.models import Group
from apps.users.serializers import UserSerializers
from .models import Exam,ExamTestCase

User = get_user_model()

class ExamSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Exam
        fields = ['pk','user','created_at']



class ExamTestCaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamTestCase
        fields = '__all__'



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


class ExamTestCaseSerializers(serializers.Serializer):
    testCaseId = serializers.IntegerField(min_value = 1)
    selectedAnswerId = serializers.IntegerField(min_value = 1)


class SubmitAnswerSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(min_value = 1)
    examTestCases = ExamTestCaseSerializers(many = True)

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        examTestCases = validated_data.get('examTestCases')

        exam = Exam.objects.create(
            user = User.objects.get(pk = user_id)
        )

        for data in examTestCases:
            testcase = data.get('testCaseId')
            answer = data.get('selectedAnswerId')

            ExamTestCase.objects.get_or_create(
                exam = exam,
                test_case = get_object_or_404(TestCase,pk = testcase),
                selected_answer = get_object_or_404(TestAnswer,pk=answer)
            )
        return exam