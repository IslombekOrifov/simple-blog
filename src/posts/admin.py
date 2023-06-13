from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'status', 'image', 'video', 'publish', 'date_created', 'date_updated', 'is_deleted']