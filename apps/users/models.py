from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class RoleChoice(models.TextChoices):
    UNKNOWN = 'unknown',"Nomalum"
    ADMIN = 'admin',"Admin"
    INSTRUCTOR = "instructor","Instructor"
    STUDENT = 'student','Student'


class User(AbstractUser):
    name = models.CharField()
    surname = models.CharField()
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='user/',null=True,blank=True,default='default/default.png')
    role = models.CharField(choices=RoleChoice.choices,default=RoleChoice.UNKNOWN)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-pk']