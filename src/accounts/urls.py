from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    # settings urls
    path('settings/account/', views.settings_account, name='settings_account'),
    path('settings/notifications/', views.settings_notifications, name='settings_notifications'),
    path('settings/privacy/', views.settings_privacy, name='settings_privacy'),
    path('settings/communications/', views.settings_communications, name='settings_communications'),
    path('settings/messaging/', views.settings_messaging, name='settings_messaging'),
    path('settings/close/account/', views.settings_close_account, name='settings_close_account'),
    # end settings urls

    # path('my/followers/', views.followers_list, name='my_followers'),
    path('my/', views.my_profile, name='my_profile'),
    path('users/profile/<username>/', views.user_detail, name='user_profile'),
    path('users/followers/<username>/', views.followers_list, name='user_followers'),

    # register login logout
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # password change
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # password reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
