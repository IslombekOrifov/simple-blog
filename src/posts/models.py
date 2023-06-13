from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from uuid import uuid4

from accounts.models import CustomUser
from accounts.validators import validate_image
from .services import upload_image_path


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
    video = models.URLField(max_length=500, blank=True, null=True)

    slug = models.SlugField(max_length=50, unique_for_date='publish')
    body = models.CharField(max_length=300, blank=True, null=True)
   
    publish = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=3, choices=PostStatus.choices, default=PostStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')


    class Meta:
        ordering = ('-date_created',)
        unique_together = ('image', 'body', 'date_created', 'publish')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.body != '':
            self.body = ' '.join(self.title.strip().split())
        if not self.slug:
            self.slug == slugify(uuid4())
        if self.body == '' and not self.image and not self.video:
            raise ValidationError("image, video yoki text to'ldirilishi kerak")
        super().save(self, *args, **kwargs)

   

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




