from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from uuid import uuid4

from .forms import PostCreateForm


@login_required
@require_POST
def post_create(request):
    post_form = PostCreateForm(request.POST)
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        post.slug = slugify(str(uuid4()))
        post.save()
        messages.add_message(request, messages.SUCCESS, "Your post has been successfully added", extra_tags="post")
        return redirect('main:index')
    else:
        messages.add_message(request, messages.ERROR, post_form.errors.as_text(), extra_tags="post")
        return redirect('main:index')