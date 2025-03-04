from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid 

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)  # Enforce unique email
    is_verified = models.BooleanField(default=False)  # Track email verification status
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta: 
        db_table = 'users'
    def __str__(self):
        return self.username
