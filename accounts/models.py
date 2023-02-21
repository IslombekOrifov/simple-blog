from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

from .validators import validate_phone, validate_image
from .services import upload_avatar_path


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=13, blank=True, validators=[validate_phone])

    REQUIRED_FIELDS = []

    avatar = models.ImageField(
        upload_to=upload_avatar_path, validators=[validate_image], 
        blank=True, null=True
    )
    about = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    other_skills = models.CharField(max_length=300, blank=True)
    hobby = models.CharField(max_length=300, blank=True)

    edu1_name = models.CharField(max_length=250, blank=True)
    edu1_direction = models.CharField(max_length=150, blank=True)
    edu1_start_date = models.DateField(blank=True, null=True)
    edu1_end_date = models.DateField(blank=True, null=True)
    edu1_now = models.BooleanField(default=False)

    edu2_name = models.CharField(max_length=250, blank=True)
    edu2_direction = models.CharField(max_length=150, blank=True)
    edu2_start_date = models.DateField(blank=True, null=True)
    edu2_end_date = models.DateField(blank=True, null=True)
    edu2_now = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email} > {self.username}'
    

    def save(self, *args, **kwargs):
        self.username = ' '.join(self.title.strip().split())
        self.email = ' '.join(self.title.strip().split())
        self.phone = ' '.join(self.title.strip().split())
        super().save(*args, **kwargs)


