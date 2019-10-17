from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='participant_index'),
    path('all_task/', views.all_available_tasks, name='participant_all_tasks'),
    path('completed_tasks/', views.index, name='participant_completed_tasks'),
]
