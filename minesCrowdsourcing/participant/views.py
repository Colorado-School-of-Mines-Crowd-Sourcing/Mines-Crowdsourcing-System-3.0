from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.detail import SingleObjectMixin
from participant.models import *
from wkhtmltopdf.views import PDFTemplateView
from django.core import mail
from django.core.mail import EmailMessage


def all_active_tasks_tags():
    all_tags_objects = Tag.objects.filter(task__status=Task.ACTIVE)
    all_tags_mapped = {}
    for tag_objects in all_tags_objects:
        try:
            all_tags_mapped[tag_objects.task] = all_tags_mapped[tag_objects.task] + \
                "," + tag_objects.tag
        except KeyError:
            all_tags_mapped[tag_objects.task] = tag_objects.tag
    return all_tags_mapped


def index(request):
    return render(request, 'participant/index.html')


def all_available_tasks(request):
    user = request.user
    all_tags_mapped = all_active_tasks_tags()
    filtered_tasks = Task.objects.filter(status=Task.ACTIVE)
        
    return render(request, 'participant/all_tasks.html', {
        'all_tasks': filtered_tasks, 'all_tags_mapped': all_tags_mapped})


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
    query_result = Task.objects.none()
    if category == 'requester':
        query_result = Task.objects.filter(
            Q(requester__name__contains=query), status=Task.ACTIVE)
    if category == 'qualifications':
        query_result = Task.objects.filter(
            Q(participant_qualifications__contains=query), status=Task.ACTIVE)
    if category == 'title':
        query_result = Task.objects.filter(
            Q(title__contains=query), status=Task.ACTIVE)
    if category == 'reward':
        try:
            query_result = Task.objects.filter(
                Q(reward_amount__gte=float(query)))
        except ValueError:
            messages.error(request, 'Please enter number value')

    if category == 'end_date':
        try:
            query_result = Task.objects.filter(
                Q(end_date__lte=datetime.strptime(query, '%m/%d/%Y')))
        except ValueError:
            messages.error(
                request, 'Please enter the date in the correct format')

    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result, 'all_tags_mapped': all_tags_mapped})


def task_details(request, task_id):
    user = request.user
    try:
        current_task = Task.objects.get(pk=task_id)
        valid_participant_task = Task.objects.filter(
             Q(major_qualifications__exact=user.major) |
             Q(major_qualifications__endswith=',%s' % user.major) |
             Q(major_qualifications__contains=',%s,' % user.major) |
             Q(major_qualifications__startswith='%s' % user.major),
             status=Task.ACTIVE, pk=task_id)
        if valid_participant_task.exists():
            valid_task = True
        else:
            valid_task = False
            

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
            message = "Thanks for completing %s for $%s. Will we contact you again when your submission has been approved." % (current_task.title, "{0:.2f}".format(current_task.reward_amount))
            body = "Mines Crowdsourcing System Task Completion: %s" % (current_task.title,)
            email_user(request.user.email, message, body)
            if current_task.participants.count() >= current_task.max_num_participants:
                current_task.status = Task.COMPLETED
            current_task.save()
            return redirect('task_details_page', task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    return render(request, 'participant/task_details.html', {'task': current_task,
                                                             'already_completed': already_completed, 'valid_task': valid_task})


def redeem(request):
    # Minimum balance to redeem
    MIN_REWARD = 5

    user = request.user

    if not user.is_authenticated:
        raise PermissionDenied()

    if request.method == 'POST':
        # Redeem all of the available balance
        amount = user.reward_balance
        #total_amount = Task.objects.filter(user_id=user.id)
        if amount >= MIN_REWARD:
            transaction = Transaction.create(user, amount)
            transaction.save()
            user.reward_balance = 0  # Reset balance to 0 since all was redeemed
            user.save()
            message = "Thanks for redeeming your balance of $%s." % ("{0:.2f}".format(amount))
            body = "Mines Crowdsourcing System Balance Redemption"
            email_user(request.user.email, message, body)
            messages.success(request, 'Your balance has been redeemed.')
        else:
            messages.error(
                request, f'You need at least ${MIN_REWARD} in order to redeem')

    return render(request, 'participant/redeem.html', {'user': user, 'min_reward': MIN_REWARD})

def email_user(user_email, message, subject):
    #email = EmailMessage(
    #    subject=subject,
    #    body=message,
    #    from_email='minescrowdsourcing@gmail.com',
    #    to=[user_email,],
    #)
    #email.send(False)
    print(subject)
    print(message)

# Admin Views
class formPDF(SingleObjectMixin, PDFTemplateView):

    model = Transaction
    template_name = 'admin/participant/transaction/transaction_form.html'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.filename = '%s.pdf' % (self.object.recipient)
        return super().get(*args, **kwargs)
