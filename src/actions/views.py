from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Action

def notifications(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    
    actions = actions.select_related('user').prefetch_related('target')

    paginator = Paginator(actions, 8)
    page = request.GET.get('page')
    actions_only = request.GET.get('actions_only')

    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if actions_only:
            return HttpResponse('')
        posactionsts = paginator.page(paginator.num_pages)
    
    if actions_only:
        return render(request, 'main/list_notif.html', {'actions': actions[:4]})


    context = {
        'actions': actions,
    }
    return render(request, 'actions/notifications.html', context)


