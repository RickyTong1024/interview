from django.shortcuts import render
from django.http import HttpResponse
from interview.models import problem_model

def problem_update(request):
    pm = problem_model()
    if request.method == 'POST':
        pass
    return render(request, 'templates/problem_update.html', {'problem' : pm})

def problem_list(request):
    return HttpResponse("problem_list")

def problem(request):
    return HttpResponse("problem")
