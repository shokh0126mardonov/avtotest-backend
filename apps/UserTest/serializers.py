from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.TestCase.models import TestAnswer, TestCase
from apps.users.serializers import UserSerializers
from apps.Group.models import Group
from apps.users.serializers import UserSerializers
from .models import Exam, ExamTestCase

User = get_user_model()


class ExamSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)

    class Meta:
        model = Exam
        fields = ["pk", "user", "created_at", "correct_answer", "total_count"]


class ExamTestCaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamTestCase
        fields = "__all__"


class UserGroupSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    group_id = serializers.IntegerField(min_value=1)


class GroupIdSerializers(serializers.Serializer):
    group_id = serializers.IntegerField(min_value=1)


class GroupUserSerializers(serializers.ModelSerializer):
    users = UserSerializers(read_only=True, many=True)

    class Meta:
        model = Group
        fields = [
            "pk",
            "name",
            "description",
            "image",
            "is_active",
            "created_date",
            "instructor",
            "users",
        ]


class ExamTestCaseSerializers(serializers.Serializer):
    testCaseId = serializers.IntegerField(min_value=1)
    selectedAnswerId = serializers.IntegerField(min_value=1)


class SubmitAnswerSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    examTestCases = ExamTestCaseSerializers(many=True)

    def validate_examTestCases(self, value):
        ids = [i["testCaseId"] for i in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError("Duplicate testCaseId")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user_id = validated_data["user_id"]
        examTestCases = validated_data["examTestCases"]

        exam = Exam.objects.create(user_id=user_id)

        testcase_ids = [i["testCaseId"] for i in examTestCases]
        answer_ids = [i["selectedAnswerId"] for i in examTestCases]

        testcases = TestCase.objects.in_bulk(testcase_ids)
        answers = TestAnswer.objects.in_bulk(answer_ids)
        correct_answer = 0

        for data in examTestCases:
            tc = testcases.get(data["testCaseId"])
            ans = answers.get(data["selectedAnswerId"])

            if not tc or not ans:
                raise serializers.ValidationError("Invalid testCaseId or answerId")

            if ans.is_correct:
                correct_answer += 1

            ExamTestCase.objects.update_or_create(
                exam=exam, test_case=tc, defaults={"selected_answer": ans}
            )

        exam.correct_answer = correct_answer
        exam.total_count = len(examTestCases)
        exam.save(update_fields=["correct_answer", "total_count"])

        return exam
