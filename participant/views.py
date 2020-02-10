from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render , redirect
from participant.models import *
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin

from wkhtmltopdf.views import PDFTemplateView

def all_active_tasks_tags():
    all_tags_objects = Tag.objects.filter(task__status=Task.ACTIVE)
    all_tags_mapped = {}
    for tag_objects in all_tags_objects:
        try:
            all_tags_mapped[tag_objects.task] = all_tags_mapped[tag_objects.task] + "," + tag_objects.tag
        except KeyError:
            all_tags_mapped[tag_objects.task] = tag_objects.tag
    return all_tags_mapped


def index(request):
    return render(request, 'participant/index.html')


def all_available_tasks(request):
    all_tags_mapped = all_active_tasks_tags()
    return render(request, 'participant/all_tasks.html', {
        'all_tasks': Task.objects.filter(status=Task.ACTIVE), 'all_tags_mapped': all_tags_mapped})


def completed_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'participant/completed_tasks.html')
    else:
        all_completed_tasks = Task.objects.filter(
            participants=user,
        )
        return render(request, 'participant/completed_tasks.html', {
            'all_completed_tasks': all_completed_tasks})


def search_results(request):
    all_tags_mapped = all_active_tasks_tags()
    query = request.GET.get('q')
    category = request.GET.get('category')
    if category == 'requester':
        query_result = Task.objects.filter(Q(requester__name__contains=query), status=Task.ACTIVE)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result, 'all_tags_mapped': all_tags_mapped})


def task_details(request, task_id):
    try:
        current_task = Task.objects.get(pk=task_id)

        # If the task has not been posted or is closed and the user
        # has not completed, we still want to display a 404
        if (current_task.status == Task.PENDING or
            (current_task.status == Task.COMPLETED
            and request.user not in current_task.participants.all()
            and request.user not in current_task.approved_participants)):
                raise Task.DoesNotExist
        already_completed = request.user in current_task.participants.all()
        if request.method == 'POST':
            messages.success(request, 'Thank you for your contribution! This task has been marked complete and is '
                                      'waiting for the approval of the requester.')
            current_task.participants.add(request.user)
            if current_task.participants.count() >= current_task.max_num_participants:
                current_task.status = Task.COMPLETED
            current_task.save()
            return redirect('task_details_page', task_id)
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


# Admin Views
class formPDF(SingleObjectMixin, PDFTemplateView):

    model = Transaction
    template_name = 'admin/participant/transaction/transaction_form.html'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.filename = '%s.pdf' % (self.object.recipient)
        return super().get(*args, **kwargs)
