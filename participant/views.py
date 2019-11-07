from django.shortcuts import render
from participant.models import *
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.http import HttpResponse
from django.contrib import messages

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
        completed_tasks = Task.objects.filter(
            participantcompletedtask__user=user
        )
        return render(request, 'participant/completed_tasks.html', {
            'completed_tasks': completed_tasks})


def search_results(request):
    query = request.GET.get('q')
    query_title = Task.objects.filter(Q(title__contains=query), is_posted=True)
    query_tag = Task.objects.filter(Q(tag__tag__contains=query), is_posted=True)
    query_result = query_tag.union(query_title)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result})


def redeem(request):
    # Minimum balance to redeem
    MIN_REWARD = 5

    user = request.user

    if request.method == 'POST':
        amount = user.reward_balance
        if amount > MIN_REWARD:
            transaction = Transaction.create(user, amount)
            transaction.save()
            user.reward_balance = 0
            user.save()
            messages.success(request, 'Your balance has been redeemed.')
        else:
            messages.error(request, f'Your need ${MIN_REWARD} in order to redeem')

    return render(request, 'participant/redeem.html', {'user':user, 'min_reward':MIN_REWARD })
