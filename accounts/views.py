from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


from .forms import LoginForm, UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
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
def index(request):
    return render(request, 'accounts/index.html')


@login_required
def settings_account(request):
    context = {
        'settings_menu_title': "account",
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