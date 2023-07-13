from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from .validators import validate_phone, validate_image
from .services import upload_avatar_path


class CustomUser(AbstractUser):
    """ Custom user model """

    custom_id = models.CharField(
        max_length=12,
        db_index=True,
        error_messages={
            "unique": _("A user with that custom_id already exists."),
        },
        unique=True,
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=13, 
        blank=True, 
        validators=[validate_phone]
    )

    REQUIRED_FIELDS = []

    first_login = models.DateField(null=True)
    middle_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(
        upload_to=upload_avatar_path, 
        validators=[validate_image], 
        blank=True, null=True
    )
    
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email} > {self.username}'
    

    def save(self, *args, **kwargs):
        self.username = ' '.join(self.username.strip().split())
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        if self.custom_id == '':
            self.custom_id = str(uuid4())[-12:]
        super().save(*args, **kwargs)


class Experience(models.Model):
    user = models.ForeignKey(CustomUser, related_name='experiences', on_delete=models.CASCADE)
    
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    work_start_date = models.DateField()
    work_end_date = models.DateField(blank=True, null=True)
    work_now = models.BooleanField(default=False)
    work_duties = models.CharField(max_length=300, blank=True)

    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.role
    

class Profile(models.Model):
    """ User's profile datas """

    class LifeStatus(models.TextChoices):
        SINGLE = 's', 'Single'
        RELATIONSHIP = 'ir', 'In relationship'

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    about = models.CharField(max_length=300, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    other_skills = models.CharField(max_length=300, blank=True)
    overview = models.CharField(max_length=100, blank=True)    
    life_status = models.CharField(
        max_length=2, 
        choices=LifeStatus.choices, 
        default=LifeStatus.SINGLE
    )

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