from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import subprocess
from django.core.files.uploadedfile import TemporaryUploadedFile


from .forms import SubmissionForm


from .models import Problem, Submission
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

    submissions = Submission.objects.all()

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():

            id = form.cleaned_data["problem_id"]
            problem = get_object_or_404(Problem, id = id)

            submission = form.cleaned_data["submission"]
            
            
            output = handle_submission(submission, problem.testcase_set.all())

            if output is True:
                verdict = "AC"
            else:
                verdict = "WA"
            
            print(verdict)

            s = Submission(problem = problem, verdict = verdict, submission = submission)
            s.save()

            submissions = Submission.objects.all()

            context = {
                "submissions" : submissions
            }

            return render(request, "submissions.html", context=context)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    
    return render(request, "submissions.html", {
        "submissions" : submissions
    })


def handle_submission(submission, testcases):

    with open('input.cpp', 'w') as destination:
        destination.write(submission)

    subprocess.run(["g++", "input.cpp", "-o", "output.exe"])

    for testcase in testcases:

        input = testcase.input
        input = bytes(input, 'utf-8')

        output = subprocess.run(['output.exe'], capture_output=True, input = input, timeout=10)
        output = output.stdout.decode("utf-8")

        if output != testcase.output:
            return False

    return True


def view_submission(request, id):
    submission = get_object_or_404(Submission, id = id)
    context = {
        'submitted_code': submission.submission
    }
    return render(request, "viewsubmission.html", context = context)