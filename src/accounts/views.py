from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import UpdateView


from .models import Experience, CustomUser, Profile
from .forms import (
    LoginForm, UserRegisterForm, CustomUserEdit,
    ProfileEdit, UserExperienceForm,
)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            Profile.objects.create(user=user)
            user = authenticate(
                                request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:my_profile')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/registration.html', {'form': form})


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change")
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_change_done'] = "Your passwod has been changed successfully"
        return context
   

class CustomPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")




@login_required
def settings_account(request):
    exper = Experience.objects.filter(user=request.user).last()
    if request.method == 'POST':
        user_form = CustomUserEdit(
            instance=request.user, data=request.POST, files=request.FILES
        )
        profile_form = ProfileEdit(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if exper:
            exper_form = UserExperienceForm(
                instance=exper,
                data=request.POST
                )
        else:
            exper_form = UserExperienceForm(data=request.POST)
        if user_form.is_valid() and profile_form.save():
            user_form.save()
    else:
        user_form = CustomUserEdit(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)
        if exper:
            exper_form = UserExperienceForm(instance=exper)
        else:
            exper_form = UserExperienceForm()

    context = {
        'settings_menu_title': "account",
        'user_form': user_form,
        'profile_form': profile_form,
        'exper_form': exper_form,
    }
    return render(request, 'accounts/settings/settings-account.html', context)


@login_required
def settings_notifications(request):
    context = {
        'settings_menu_title': "notifications",
    }
    return render(request, 'accounts/settings/settings-notifications.html', context)


@login_required
def settings_privacy(request):
    context = {
        'settings_menu_title': "privacy",
    }
    return render(request, 'accounts/settings/settings-privacy.html', context)

@login_required
def settings_communications(request):
    context = {
        'settings_menu_title': "communications",
    }
    return render(request, 'accounts/settings/settings-communications.html', context)


@login_required
def settings_messaging(request):
    context = {
        'settings_menu_title': "messaging",
    }
    return render(request, 'accounts/settings/settings-messaging.html', context)


@login_required
def settings_close_account(request):
    context = {
        'settings_menu_title': "close_account",
    }
    return render(request, 'accounts/settings/settings-close-account.html', context)


@login_required
def my_profile(request):
    context = {
        'settings_menu_title': "close_account",
    }
    return render(request, 'accounts/my-profile.html', context)


@login_required
def user_profile(request, custom_id):
    user = CustomUser.objects.filter(custom_id=custom_id).select_related('profile').first()
    if not user:
        raise Http404("Sorry. this user didn't match")
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def followers_list(request, username):
    user = CustomUser.objects.filter(username=username).select_related('profile').prefetch_related('followers').first()
    if not user:
        raise Http404
    return render(request, 'accounts/followers.html', {'user': user})


@login_required
def user_detail(request, username):
    user = CustomUser.objects.filter(username=username, is_deleted=False, is_active=True).select_related('profile').first()
    if not user:
        raise Http404
    return render(request, 'accounts/profile.html', {'user': user})