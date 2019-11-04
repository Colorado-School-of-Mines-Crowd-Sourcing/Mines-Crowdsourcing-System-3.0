from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='participant_index'),
    path('all_task/', views.all_available_tasks, name='participant_all_tasks'),
    path('completed_tasks/', views.completed_tasks, name='participant_completed_tasks'),
    path('search_result/', views.search_results, name='search_on_all_tasks'),
    re_path(r'^task_details/task', views.task_details, name='task_details_page'),
]
