from django.db import models
import uuid

def roadsign_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'RoadSign/{uuid.uuid4()}.{ext}'

def roadsingfolder_upload_path(instance,filename):
    ext = filename.split('.')[-1]
    return f'RoadSignFolder/{uuid.uuid4()}.{ext}'

class RoadSignFolder(models.Model):    
    name = models.CharField(max_length=255,unique=True)
    icon_path = models.ImageField(upload_to=roadsingfolder_upload_path)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'road_sign_folders'
        indexes = [
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return self.name or "Unnamed Folder"
    

class RoadSign(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, null=True, blank=True)
    icon_path = models.ImageField(upload_to=roadsign_upload_path)
    description = models.TextField(null=True, blank=True)

    folder = models.ForeignKey(
        RoadSignFolder,
        on_delete=models.CASCADE,
        related_name='road_signs'
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'road_signs'
        indexes = [
            models.Index(fields=['folder']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return self.name or "Unnamed RoadSign"