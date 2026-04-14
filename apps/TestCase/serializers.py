import os
from rest_framework import serializers

from .models import TestCase,TestAnswer


class TestCaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

    def validate_media(self, attrs):
        allowed = ['.mp3','.jpeg','.jpg','.png','.mp4']
        
        data_type = os.path.splitext(attrs.name)[1].lower()

        if data_type not in allowed:
            raise serializers.ValidationError('ruxsat etilmagan file turi',400)
        
        return attrs

