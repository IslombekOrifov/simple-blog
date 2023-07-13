from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from posts.models import Post
from posts.forms import PostCreateForm


@login_required
def index(request):
    post_form = PostCreateForm()
    posts = Post.objects.all()
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    posts_only = request.GET.get('posts_only')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if posts_only:
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    
    if posts_only:
        return render(request, 'main/list_post.html', {'posts': posts})

    context = {
        'post_form': post_form,
        'posts': posts,
    }
    return render(request, 'main/index.html', context)