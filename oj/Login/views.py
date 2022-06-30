from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import subprocess
from django.core.files.uploadedfile import TemporaryUploadedFile


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

    solutions = Solution.objects.all()

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():

            id = form.cleaned_data["problem_id"]
            problem = get_object_or_404(Problem, id = id)
            file = request.FILES["solution"]
            
            output = handle_uploaded_file(file, problem.testcase_set.all())

            if output is True:
                verdict = "AC"
            else:
                verdict = "WA"
            
            print(verdict)

            s = Solution(problem = problem, verdict = verdict, solution_file = file)
            s.save()

            solutions = Solution.objects.all()

            context = {
                "solutions" : solutions
            }

            return render(request, "submissions.html", context=context)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
    return render(request, "submissions.html", {
        "solutions" : solutions
    })


def handle_uploaded_file(file, testcases):

    with open('input.cpp', 'wb+') as destination:
        for chunk in file.chunks():
            print(chunk)
            destination.write(chunk)

    subprocess.run(["g++", "input.cpp", "-o", "output.exe"])

    for testcase in testcases:

        input = testcase.input
        input = bytes(input, 'utf-8')

        output = subprocess.run(['output.exe'], capture_output=True, input = input, timeout=10)
        output = output.stdout.decode("utf-8")

        if output != testcase.output:
            return False

    return True


