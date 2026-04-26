from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="groups/", null=True, blank=True)

    instructor = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructed_groups",
        unique=True,
    )

    users = models.ManyToManyField(User, related_name="group", blank=True)

    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "User Group"

    def __str__(self):
        return self.name or str(self.id)
