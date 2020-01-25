from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps
from django.http import Http404, QueryDict

from participant.models import User, Task, Tag
from .forms import CreateTask, CreateApproval

def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_task = CreateTask(request.POST)
        # check whether it's valid
        if form_task.is_valid() :
            # Task creation
            new_task = form_task.save(commit=False)
            new_task.requester = request.user
            new_task.save()

            # Tag creation
            for tag in request.POST.get('tags').split(','):
                logger.info(request, 'tag ', tag, ' created')
                new_tag = Tag.create(tag, new_task)
                new_tag.save()

            messages.success(request, 'Your task has been submitted for review.')
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
            status = Task.PENDING,
        )

        active = Task.objects.filter(
            requester = user,
            status = Task.ACTIVE,
        )

        completed = Task.objects.filter(
            requester = user,
            status = Task.COMPLETED,
        )

        return render(request, 'requester/tasks.html', {
            'pending': pending,
            'active': active,
            'completed': completed,
        })

def approve(task_id, request):
    form_approval = CreateApproval(request.POST)
    if form_approval.is_valid():
        users = form_approval.cleaned_data['participants']
        for user in users:
            if user not in task.approved_participants.all():
                user.reward_balance += task.reward_amount
                task.approved_participants.add(user)
                user.save()
        task.save()
        messages.success(request, 'The participants you selected are now approved!')
        return redirect('contributor_approval', task_id)

def close(task_id):
    task.status = Task.COMPLETED
    task.save()
    messages.success(request, 'The task has been closed!')
    return redirect('contributor_approval', task_id)

def approve_contributors(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        if task.requester != request.user:
            raise Task.DoesNotExist

        if request.method == 'POST':
            if 'approve' in request.POST:
                return approve(task_id, request)
            elif 'close' in request.POST:
                return close(task_id)
        else:
            participants_set=task.participants.all().difference(task.approved_participants.all())
            form_approval = CreateApproval(participants_set=participants_set)
            approval_left = True
            if participants_set.count() == 0:
                approval_left = False
            return render(request, 'requester/approval.html',
                        {'form_approval': form_approval,
                        'task': task,
                        'approval_left': approval_left,})
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
