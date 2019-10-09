from django.shortcuts import render
from django.http import HttpResponse

from .forms import CreateJob

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateJob(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_job = form.save()
            new_job.requester = request.user
            new_job.save()
            messages.success(request, "Your task has been submitted for review.")
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateJob()

    return render(request, 'requester/index.html', {'form': form})
