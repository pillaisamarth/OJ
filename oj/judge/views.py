from codecs import unicode_escape_encode
import filecmp
from re import L
import sys
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import subprocess
import os
from django.core.files.storage import FileSystemStorage
from oj import settings


from .forms import SubmissionForm


from .models import Problem, Submission, testcase_output
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
    problem = get_object_or_404(Problem, id = id)
    form = SubmissionForm()
    context = {
        "problem" : problem,
        "form" : form,
    }
    return render(request, "problemdetail.html", context = context)

def submit(request):
    
    form = SubmissionForm(request.POST, request.FILES)
    folder = os.path.join(settings.FILE_PATH_FIELD_DIR, 'submissions')
    

    if form.is_valid():
        count = Submission.objects.all().count()
        filefolder = os.path.join(folder, str(count + 1))
        os.mkdir(filefolder)

        submission = form.cleaned_data["submission"]
        fs = FileSystemStorage(location=filefolder)
        filename_with_extension = fs.save(name=submission.name, content = submission)
        filename = os.path.splitext(filename_with_extension)[0]


        problem_id = request.POST.get("problem_id")
        problem = get_object_or_404(Problem, id = problem_id)
        language = form.cleaned_data["language"]
        

        if language == 'cpp':
            path = os.path.join(filefolder, filename)
            subprocess.run(["cmd", "/c", f"g++ {path}.cpp -o {path}.exe"])
        elif language == 'java':
            path = os.path.join(filefolder, filename)
            subprocess.run(["cmd", "/c", f"javac {path}.java"])

        testcases = problem.testcase_set.all()

        verdict="AC"

        print(filename)


        for testcase in testcases:
            input = open(testcase.input, 'r')
            oppath = os.path.join(folder, 'output.txt')
            op = open(oppath, 'w')
            if language == 'cpp':
                path = os.path.join(filefolder, filename)
                output = subprocess.Popen(f"{path}.exe",
                 stdin=input, stdout=op)
                ret = output.wait()
                op.flush()
            elif language == 'java':
                output = subprocess.Popen(f"java -cp {filefolder} {filename}",
                stdin = input, stdout=op)
                ret = output.wait()
                op.flush()
            else:
                path = os.path.join(filefolder, filename)
                output = subprocess.Popen(f"py {path}.py",
                stdin = input, stdout=op)
                ret = output.wait()
                op.flush()
            
            

           
            if filecmp.cmp(oppath, testcase.output) != True:
                verdict = "WA"
                break
        
        path = os.path.join(filefolder, filename_with_extension)
        submission=Submission(problem = problem, verdict = verdict, language = language, submission = path)
        submission.save()
        print(verdict)

        

            

        


    return HttpResponse(verdict)
            



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