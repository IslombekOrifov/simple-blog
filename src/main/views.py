from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from posts.forms import PostCreateForm

@login_required
def index(request):
    post_form = PostCreateForm()
    context = {
        'post_form': post_form,
    }
    return render(request, 'main/index.html', context)