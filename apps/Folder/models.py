import os

from django.db import models
from uuid import uuid4



class Folder(models.Model):
    name = models.CharField(max_length=128,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} {self.created_at}"
    class Meta:
        ordering = ['-pk']



def media_file_upload_path(instanse,filename):
    print(filename)
    ext = filename.split('.')[-1]
    return f"Folder/{uuid4()}.{ext}"


class MediaFile(models.Model):
    
    file = models.FileField(
        upload_to=media_file_upload_path
    )

    file_name = models.CharField(
        max_length=255,
        blank=True
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
    )

    created_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.file_name or self.file.name