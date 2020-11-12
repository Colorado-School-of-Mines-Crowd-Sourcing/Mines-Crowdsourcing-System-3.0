from django.apps import apps
from django.contrib import messages
from django.http import Http404, QueryDict
from django.shortcuts import redirect, render
from django.core import mail
from django.core.mail import EmailMessage

from participant.models import Tag, Task, User

from .forms import CreateApproval, CreateTask


def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_task = CreateTask(request.POST)
        # check whether it's valid
        if form_task.is_valid():
            # Task creation
            new_task = form_task.save(commit=False)
            new_task.requester = request.user
            new_task.save()

            # Tag creation
            for tag in request.POST.get('tags').split(','):
                new_tag = Tag.create(tag, new_task)
                new_tag.save()

            messages.success(
                request, 'Your task has been submitted for review.')
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
            requester=user,
            status=Task.PENDING,
        )

        active = Task.objects.filter(
            requester=user,
            status=Task.ACTIVE,
        )

        completed = Task.objects.filter(
            requester=user,
            status=Task.COMPLETED,
        )
        
        tasks = Task.objects.filter(
            requester=user,
        )
        class TaskInfo:
           def __init__(self, title, total_paid, percent_complete, reward_amount, num_completed):
            self.title = title
            self.total_paid = total_paid
            self.percent_complete = percent_complete
            self.reward_amount = reward_amount
            self.num_completed = num_completed

        task_data = []
        for task in tasks:
            title = task.title
            num_completed = task.participants.all().count()
            num_approved = task.approved_participants.count() + task.paid_participants.count()
            total_paid = num_approved * task.reward_amount
            percent_complete = "{0:.2f}".format(num_approved / task.max_num_participants * 100)
            task_info = TaskInfo(title, total_paid, percent_complete, task.reward_amount, num_completed)
            task_data.append(task_info)

        return render(request, 'requester/tasks.html', {
            'pending': pending,
            'active': active,
            'completed': completed,
            'task_data': task_data,
        })


def approve(task, task_id, request):
    form_approval = CreateApproval(request.POST)
    if form_approval.is_valid():
        users = form_approval.cleaned_data['participants']
        for user in users:
            if user not in task.approved_participants.all():
                user.reward_balance += task.reward_amount
                task.approved_participants.add(user)
                message = "Your submission for %s has been approved. $%s has been added to your account." % (task.title, "{0:.2f}".format(task.reward_amount))
                body = "Mines Crowdsourcing System Task Approval - %s" % (task.title,)
                email_user(request, message, body)
                user.save()
        task.save()
        messages.success(
            request, 'The participants you selected are now approved!')
        return redirect('contributor_approval', task_id)


def close(task, task_id, request):
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
                return approve(task, task_id, request)
            elif 'close' in request.POST:
                return close(task, task_id, request)
        else:
            participants_set = task.participants.all().difference(
                task.approved_participants.all())
            form_approval = CreateApproval(participants_set=participants_set)
            num_completed = task.participants.all().count()
            num_approved = task.approved_participants.count() + task.paid_participants.count()
            total_paid = num_approved * task.reward_amount
            percent_complete = "{0:.2f}".format(num_approved / task.max_num_participants * 100)
            success_rate = "{0:.2f}".format(num_approved / num_completed * 100)
            approval_left = True
            if participants_set.count() == 0:
                approval_left = False
            return render(request, 'requester/approval.html',
                          {'form_approval': form_approval,
                           'task': task,
                           'approval_left': approval_left,
                           'num_completed': num_completed,
                           'num_approved': num_approved, 
                           'total_paid': total_paid,
                           'percent_complete': percent_complete,
                           'success_rate': success_rate, })
    except Task.DoesNotExist:
        raise Http404('Task does not exist')

def email_user(user_email, message, subject):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='minescrowdsourcing@gmail.com',
        to=[user_email,],
    )
    email.send(False)
