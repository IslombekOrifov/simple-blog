from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from uuid import uuid4

from accounts.models import CustomUser
from accounts.validators import validate_image
from .services import upload_image_path

from .enums import PostStatus, CommentStatus

# Create your models here.
class Post(models.Model):
    image = models.ImageField(upload_to=upload_image_path, validators=[validate_image], 
                              blank=True, null=True
                              )
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    body = models.TextField(blank=True)
   
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')

    publish = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=3, choices=PostStatus.choices(), default=PostStatus.ac.name)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_created',)
        unique_together = ('image', 'title', 'date_created', 'publish')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title != '':
            self.title = ' '.join(self.title.strip().split())
        if not self.id:
            self.slug == slugify(uuid4())

        if self.title == '' and not self.image:
            raise ValidationError("image yoki title to'ldirilishi kerak")
        super().save(self, *args, **kwargs)

   

class Comment(models.Model):
    body = models.CharField(max_length=150)
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='childs')
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=3, choices=PostStatus.choices(), default=PostStatus.ac.name)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        self.body = ' '.join(self.title.strip().split())
        super().save(self, *args, **kwargs)

class Like(models.Model):    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)




