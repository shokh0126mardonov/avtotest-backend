from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class RoleChoice(models.TextChoices):
    ADMIN = 'admin',"Admin"
    INSTRUCTOR = "instructor","Instructor"
    STUDENT = 'student','Student'


class User(AbstractUser):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=RoleChoice.choices)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    image = models.ImageField(upload_to='user/',null=True,blank=True,default='default/default.png')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} {self.username}"
    
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



from django.db import models
from django.conf import settings

class DeviceLock(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_lock",
    )

    telegram_id = models.BigIntegerField(null=True,blank=True)
    device_id   = models.CharField(max_length=255,null=True)   
    user_agent  = models.CharField(max_length=300,null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.device_id}"
