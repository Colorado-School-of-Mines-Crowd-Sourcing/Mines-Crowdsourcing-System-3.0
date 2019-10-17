from django.urls import path

from . import views

urlpatterns = [
    path('', views.create, name='requester_create'),
    path('tasks', views.see_tasks, name='requester_tasks',)
]
