from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from uuid import uuid4

from accounts.models import CustomUser
from accounts.validators import validate_image
from .services import upload_image_path, upload_video_path


class Post(models.Model):

    class PostStatus(models.TextChoices):
        ACTIVE = 'ac', 'Active'
        NOTACTIVE = 'na', 'Not Active'
        ARCHIVE = 'ar', 'Archive'
        BANNED = 'bn', 'Banned'

    image = models.ImageField(upload_to=upload_image_path, 
                              validators=[validate_image], 
                              blank=True, null=True
                             )
    video = models.FileField(upload_to=upload_video_path, blank=True, null=True)

    slug = models.SlugField(max_length=50, unique=True)
    text = models.CharField(max_length=300, blank=True, null=True)
   
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=3, choices=PostStatus.choices, default=PostStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0, blank=True)

    users_like = models.ManyToManyField(CustomUser, related_name='images_liked', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')


    class Meta:
        ordering = ('-date_created',)
        unique_together = ('image', 'text', 'date_created',)
        indexes = [
            models.Index(fields=['-date_created', 'slug', 'status']),
        ]


    def save(self, *args, **kwargs):
        # Clean the text field by removing extra spaces
        if self.text:
            self.text = ' '.join(self.text.strip().split())

        # Generate a unique slug using UUID if it's not provided
        if not self.slug:
            self.slug = slugify(uuid4())

        # Check if either text, image, or video is provided
        if not self.text and not self.image and not self.video:
            raise ValidationError("Image, video, or text must be provided.")
        
        # Call the original save method with the modified data
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("posts:detail", args=[self.id, self.slug])
   

class Comment(models.Model):

    class CommentStatus(models.TextChoices):
        ACTIVE = 'ac', 'Active'
        BANNED = 'bn', 'Banned'
    
    body = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=CommentStatus.choices, default=CommentStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='childs')
    

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        self.body = ' '.join(self.body.strip().split())
        super().save(self, *args, **kwargs)


class Like(models.Model):    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)




