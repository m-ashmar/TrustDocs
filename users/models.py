from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import models

class User(AbstractUser):
    NATIONAL_ID_LENGTH = 10

    USER_TYPES = [
        ('citizen', 'Citizen'),
        ('institution', 'Institution'),
    ]

    national_id = models.CharField(max_length=NATIONAL_ID_LENGTH, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set")

    def __str__(self):
        return f"{self.username} - {self.user_type}"

