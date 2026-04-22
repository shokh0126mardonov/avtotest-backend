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
        fields = ['pk','user','created_at','correct_answer','total_count']



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

        total_test = len(examTestCases)
        correct_answer = 0

        for data in examTestCases:
            testcase_id = data.get('testCaseId')
            answer_id = data.get('selectedAnswerId')

            testcase = get_object_or_404(TestCase,pk=testcase_id)
            selected_answer = get_object_or_404(TestAnswer,pk=answer_id)

            if selected_answer.is_correct:
                correct_answer += 1

            ExamTestCase.objects.get_or_create(
                exam = exam,
                test_case = testcase,
                selected_answer = selected_answer
            )
        exam.correct_answer = correct_answer
        exam.total_count = total_test
        exam.save()

        return {
                "exam_id": exam.id,
                "correct_answers": exam.correct_answer,
                "total_questions": exam.total_count
            }