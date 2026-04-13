from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class RoleChoice(models.TextChoices):
    ADMIN = 'admin',"Admin"
    INSTRUCTOR = "instructor","Instructor"
    STUDENT = 'student','Student'


class User(AbstractUser):
    name = models.CharField()
    surname = models.CharField()
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='user/',null=True,blank=True,default='default/default.png')
    role = models.CharField(choices=RoleChoice.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    @property
    def admin(self):
        return self.role == RoleChoice.ADMIN
    
    @property
    def instructor(self):
        return self.role == RoleChoice.INSTRUCTOR
    
    @property
    def student(self):
        return self.role == RoleChoice.STUDENT
    
    @property
    def unknow(self):
        return self.role == RoleChoice.UNKNOWN
    
    class Meta:
        ordering = ['-pk']

