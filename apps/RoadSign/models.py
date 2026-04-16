from django.db import models


class RoadSignFolder(models.Model):    
    name = models.CharField(max_length=255)
    icon_path = models.ImageField(upload_to='RoadSignFolder/')

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
    icon_path = models.ImageField(upload_to='RoadSign/')
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