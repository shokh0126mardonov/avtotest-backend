from rest_framework import serializers

from .models import Folder,MediaFile

class FolderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class MediaFileSerializers:
    class Meta:
        model = MediaFile
        fields = '__all__'