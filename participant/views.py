from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect
from participant.models import *
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request, 'participant/index.html')


def all_available_tasks(request):
    return render(request, 'participant/all_tasks.html', {
        'all_tasks': Task.objects.filter(is_posted=True)})


def completed_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'participant/completed_tasks.html')
    else:
        all_completed_tasks = Task.objects.filter(
            participantcompletedtask__user=user
        )
        return render(request, 'participant/completed_tasks.html', {
            'all_completed_tasks': all_completed_tasks})


def search_results(request):
    query = request.GET.get('q')
    query_title = Task.objects.filter(Q(title__contains=query), is_posted=True)
    query_tag = Task.objects.filter(Q(tag__tag__contains=query), is_posted=True)
    query_result = query_tag.union(query_title)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result})

def task_details(request, task_id):
    try:
        current_task = Task.objects.get(is_posted=True, pk=task_id)
        already_completed = False
        if request.method == 'POST':
            ParticipantCompletedTask.create(request.user, current_task).save()
            messages.success(request, 'Thank you for your contribution! This task has been marked complete and is '
                                      'waiting for the approval of the requester.')
            return redirect('task_details_page', task_id)
        try:
            ParticipantCompletedTask.objects.get(task=current_task)
            already_completed = True
        except ObjectDoesNotExist:
            pass
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    return render(request, 'participant/task_details.html', {'task': current_task,
                                                             'already_completed': already_completed})
  
def redeem(request):
    # Minimum balance to redeem
    MIN_REWARD = 5

    user = request.user

    if not user.is_authenticated:
        raise PermissionDenied()

    if request.method == 'POST':
        # Redeem all of the available balance
        amount = user.reward_balance
        if amount >= MIN_REWARD:
            transaction = Transaction.create(user, amount)
            transaction.save()
            user.reward_balance = 0  # Reset balance to 0 since all was redeemed
            user.save()
            messages.success(request, 'Your balance has been redeemed.')
        else:
            messages.error(request, f'You need at least ${MIN_REWARD} in order to redeem')

    return render(request, 'participant/redeem.html', {'user': user, 'min_reward': MIN_REWARD})