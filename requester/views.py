from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps

from participant.models import User, Task, RequesterActiveTask, RequesterPastTask, Tag
from .forms import CreateTask

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
        # check whether it's valid:
        print(request)
        if form_task.is_valid() :
            # Task creation
            new_task = form_task.save(commit=False)
            new_task.requester = request.user
            new_task.save()
            RequesterActiveTask.create(new_task.requester, new_task).save()

            # Tag creation
            for tag in request.POST.get('tags').split():
                logger.info(request, "tag ", tag, " created")
                new_tag = Tag.create(tag, new_task)
                new_tag.save()

            logger.info(request, "task submitted for review.")
            messages.success(request, "Your task has been submitted for review.")
            return redirect('requester_create')

    # if a GET (or any other method) we'll create a blank form
    else:
        form_task = CreateTask()
    return render(request, 'requester/create.html', {'form_task': form_task})

def see_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'requester/tasks.html')
    else:
        pending = Task.objects.filter(
            requester = user,
            requesteractivetask__task__is_posted = False
        )

        active = Task.objects.filter(
            requester = user,
            requesteractivetask__task__is_posted = True
        )

        completed = Task.objects.filter(
            requesterpasttask__user = user
        )

        return render(request, 'requester/tasks.html', {
            'pending': pending,
            'active': active,
            'completed': completed,
        })
