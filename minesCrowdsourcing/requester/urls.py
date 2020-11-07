from django.urls import path, re_path

from . import views

urlpatterns = [
    path('create', views.create, name='requester_create'),
    path('', views.see_tasks, name='requester_tasks',),
    re_path(r'^(?P<task_id>\d+)/$', views.approve_contributors, name='contributor_approval'),
]
