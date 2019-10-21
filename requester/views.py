from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps

from participant.models import User, Task, RequesterActiveTask, RequesterPastTask
from .forms import CreateTask, CreateTags

# TODO: Remove random import when user authentication is done
import random, string

# Logger
import logging

logger = logging.getLogger(__name__)
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_task = CreateTask(request.POST)
        form_tags = CreateTask(request.POST)
        # check whether it's valid:
        if form_task.is_valid() and form_tags.is_valid():
            new_job = form_task.save(commit=False)
            new_job.requester = request.user
            new_job.save()
            RequesterActiveTask.create(new_job.requester, new_job).save()
            logger.info(request, "task submitted for review.")
            messages.success(request, "Your task has been submitted for review.")
            return redirect('requester_create')

    # if a GET (or any other method) we'll create a blank form
    else:
        form_task = CreateTask()
        form_tags = CreateTags()

    return render(request, 'requester/create.html', {'form_task': form_task, 'form_tags': form_tags})

def see_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'requester/tasks.html')
    else:
        pending = RequesterActiveTask.objects.filter(
            user = user,
            task__is_posted = False
        )

        active = RequesterActiveTask.objects.filter(
            user = user,
            task__is_posted = True
        )

        completed = RequesterPastTask.objects.filter(
            user = user
        )

        return render(request, 'requester/tasks.html', {
            'pending': pending,
            'active': active,
            'completed': completed,
        })
