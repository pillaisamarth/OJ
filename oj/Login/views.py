from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import SubmissionForm


from .models import Problem, Solution
# Create your views here.

def login(request):
    return HttpResponse("hello!")

def problemlist(request):
    problems = Problem.objects.all()
    
    context = {
        "problems" : problems
    }
    return render(request, 'problemlist.html', context = context)

def problemdetail(request, id):
    print(id)
    problem = get_object_or_404(Problem, id = id)
    print(problem)
    form = SubmissionForm()
    context = {
        "problem" : problem,
        "form" : form,
    }
    return render(request, "problemdetail.html", context = context)

def submit(request):

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data["problem_id"]
            problem = get_object_or_404(Problem, id = id)
            print(problem)
            s = Solution(solution_file = form.cleaned_data["solution"], problem = problem,
            verdict = "trial")
            s.save()

            return HttpResponse("Thanks for submitting!")
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
