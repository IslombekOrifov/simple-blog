from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from uuid import uuid4

from .models import Post
from .forms import PostCreateForm

from actions.utils import create_action



@login_required
@require_POST
def post_create(request):
    post_form = PostCreateForm(data=request.POST, files=request.FILES)
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        post.slug = slugify(str(uuid4()))
        post.save()
        create_action(request.user, "new post", post)
        messages.add_message(request, messages.SUCCESS, "Your post has been successfully added", extra_tags="post")
        return redirect('main:index')
    else:
        messages.add_message(request, messages.ERROR, post_form.errors.as_text(), extra_tags="post")
        return redirect('main:index')
    


def post_detail(request, pk, slug):
    post = Post.objects.filter(id=pk, slug=slug).select_related('author').first()
    context = {
        'post': post,
    }
    a = 9 * 866545
    return render(request, 'posts/post-details.html', )


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})