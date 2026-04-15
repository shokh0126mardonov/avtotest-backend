import os
from rest_framework import serializers
from django.db import transaction


from .models import TestCase,TestAnswer

class TestAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TestAnswer
        exclude = ['test_case']



class TestCaseSerializers(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = [
            'id',
            'question',
            'explanation',
            'media',
            'created_at'
        ]

    def validate_media(self, attrs):
        allowed = ['.mp3','.jpeg','.jpg','.png','.mp4']
        
        data_type = os.path.splitext(attrs.name)[1].lower()

        if data_type not in allowed:
            raise serializers.ValidationError('ruxsat etilmagan file turi',400)
        
        return attrs


    def get_question(self, obj):
        lang = self.context.get('lang', 'uz')

        if lang == 'ru':
            return obj.question_ru
        elif lang == 'uzk':
            return obj.question_uzk
        return obj.question_uz

    def get_explanation(self, obj):
        lang = self.context.get('lang', 'uz')

        if lang == 'ru':
            return obj.explanation_ru
        elif lang == 'uzk':
            return obj.explanation_uzk
        return obj.explanation_uz
    

class TestCaseCreateSerializers(serializers.ModelSerializer):
    answers = TestAnswerSerializer(many=True)

    class Meta:
        model = TestCase
        fields = [
            'id',
            'question_uz',
            'question_uzk',
            'question_ru',
            'explanation_uz',
            'explanation_uzk',
            'explanation_ru',
            'media',
            'answers'
        ]

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')

        test_case = TestCase.objects.create(**validated_data)

        answers = [
            TestAnswer(test_case=test_case, **answer)
            for answer in answers_data
        ]

        TestAnswer.objects.bulk_create(answers)

        return test_case
    
    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)

        # 🔹 parent update
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if answers_data is not None:
            with transaction.atomic():
                existing_answers = {a.id: a for a in instance.answers.all()}
                incoming_ids = []

                for answer_data in answers_data:
                    answer_id = answer_data.get('id')

                    # 🔹 UPDATE
                    if answer_id and answer_id in existing_answers:
                        answer = existing_answers[answer_id]
                        for attr, value in answer_data.items():
                            setattr(answer, attr, value)
                        answer.save()
                        incoming_ids.append(answer_id)

                    # 🔹 CREATE
                    else:
                        new_answer = TestAnswer.objects.create(
                            test_case=instance,
                            **answer_data
                        )
                        incoming_ids.append(new_answer.id)

                # 🔥 DELETE (DB’da bor, request’da yo‘q)
                for answer_id, answer in existing_answers.items():
                    if answer_id not in incoming_ids:
                        answer.delete()

        return instance