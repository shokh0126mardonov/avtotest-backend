import os
from rest_framework import serializers

from .models import Folder,MediaFile

class FolderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class MediaFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'

    def validate_file(self, attrs):
        allowed = ['.mp3','.jpeg','.jpg','.png','.mp4']

        data_type = os.path.splitext(attrs.name)[1].lower()

        if data_type not in allowed:
            raise serializers.ValidationError('Ruxsat etilmagan file turi!',400)
        
        return attrs