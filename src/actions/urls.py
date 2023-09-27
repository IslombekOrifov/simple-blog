from django.urls import path

from . import views

app_name = 'actions'


urlpatterns = [
    path('notifications', views.notifications, name='notif'),

]
