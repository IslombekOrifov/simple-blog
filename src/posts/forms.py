from typing import Any
from django import forms 
from django.conf import settings

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'video', 'text']

    def clean_image(self):
        if self.cleaned_data.get('image', False) and self.cleaned_data.get('video', False):
            return forms.ValidationError("You can upload only one of image or video.")
        return self.cleaned_data['image']

    
