from rest_framework import serializers

from .models import RoadSign,RoadSignFolder

class RoadSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSign
        fields = '__all__'

class RoadSignFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSignFolder
        fields = '__all__'