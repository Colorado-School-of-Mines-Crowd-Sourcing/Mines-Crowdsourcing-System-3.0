from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps

from participant.models import User, Task, RequesterActiveTask, RequesterPastTask
from .forms import CreateJob

# TODO: Remove random import when user authentication is done
import random, string

# Logger
import logging

logger = logging.getLogger(__name__)
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateJob(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_job.requester = request.user
            new_job.requester = user
            new_job.save()
            RequesterActiveTask.create(user, new_job).save()
            logger.info(request, "task submitted for review.")
            messages.success(request, "Your task has been submitted for review.")
            return redirect('requester_create')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateJob()

    return render(request, 'requester/create.html', {'form': form})

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
