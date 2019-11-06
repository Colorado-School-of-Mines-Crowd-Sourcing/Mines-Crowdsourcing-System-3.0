from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='requester_create'),
    path('', views.see_tasks, name='requester_tasks',)
]
