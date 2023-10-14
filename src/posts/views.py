from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.conf import settings
from uuid import uuid4

import redis

from actions.utils import create_action

from .models import Post
from .forms import PostCreateForm


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


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
    total_views = r.incr(f'post:{post.id}:views')
    r.zincrby('post_ranking', 1, post.id)
    context = {
        'post': post,
        'total_views': total_views,
    }
    return render(request, 'posts/post-details.html', context)


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


@login_required
def post_ranking(request):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(Post.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking.index(x.id))
    return render(request, 'main/most_viewed.html', {'most_viewed': most_viewed})