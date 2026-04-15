import os
from rest_framework import serializers

from .models import TestCase,TestAnswer


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