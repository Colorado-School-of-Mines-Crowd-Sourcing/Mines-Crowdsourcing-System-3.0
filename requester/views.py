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
            # TODO: remove following lines when authentication works
            new_job = form.save(commit=False)
            random_username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            user = User.objects.create_user(random_username, 'test', 'test@test.mines', random.randint(0, 2000), True)
            #new_job.requester = request.user
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
    # TODO: remove following lines when authentication works
    users = User.objects.all().order_by('?')
    user = users[0]
    #user = request.user

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
