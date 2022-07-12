from codecs import unicode_escape_encode
import filecmp
from multiprocessing import context
from re import L
import sys
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import subprocess
import os
from django.core.files.storage import FileSystemStorage
from oj import settings
import docker


from .forms import SubmissionForm


from .models import Problem, Submission, testcase_output
# Create your views here.

def login(request):
    return HttpResponse("hello!")

def problemlist(request):
    problems = Problem.objects.all()
    print(request.user)
    
    context = {
        "problems" : problems
    }
    return render(request, 'problemlist.html', context = context)

def problemdetail(request, id):

    print(request.user)
    problem = get_object_or_404(Problem, id = id)
    form = SubmissionForm()
    context = {
        "problem" : problem,
        "form" : form,
    }
    return render(request, "problemdetail.html", context = context)


def submit(request):

    if not request.user.is_authenticated:
        next = request.META.get('HTTP_REFERER')
        return redirect('%s?next=%s'%(settings.LOGIN_URL, next))


    
    form = SubmissionForm(request.POST, request.FILES)
    folder = os.path.join(settings.FILE_PATH_FIELD_DIR, 'submissions')


    

    if form.is_valid():
        count = Submission.objects.all().count()
        filefolder = os.path.join(folder, str(count + 1))
        if os.path.isdir(filefolder)==False:
            os.mkdir(filefolder)

        submission = form.cleaned_data["submission"]
        fs = FileSystemStorage(location=filefolder)
        filename_with_extension = fs.save(name=submission.name, content = submission)
        filename = os.path.splitext(filename_with_extension)[0]


        problem_id = request.POST.get("problem_id")
        problem = get_object_or_404(Problem, id = problem_id)
        language = form.cleaned_data["language"]
        
        if language == 'java':
            path = os.path.join(filefolder, filename)
            subprocess.run(["cmd", "/c", f"javac {path}.java"])

        testcases = problem.testcase_set.all()

        verdict="AC"

        for testcase in testcases:
            input = open(testcase.input, 'r')
            inpath = os.path.join(filefolder, 'input.txt')
            inp = open(inpath, 'w')
            for line in input:
                inp.write(line)

            inp.close()

            if language == 'cpp':
                client = docker.from_env()
                container = client.containers.run('cpmaker',
                 f'cpp_ex.sh {filename_with_extension} input.txt',
                 volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')

            outpath = os.path.join(filefolder, 'out.txt')
            f = open(outpath, 'r')
            r = open(testcase.output, 'r')

            
            
            if  f.read()!= r.read():
                print(testcase.output)
                verdict = "WA"
                break

            f.close()
            r.close()
        
        path = os.path.join(filefolder, filename_with_extension)
        submission=Submission(problem = problem, verdict = verdict, language = language, submission = path)
        submission.save()

    return HttpResponseRedirect(reverse('submissions', args=[str(problem_id)]))


def submissions(request, id):
    
    submissions = Submission.objects.filter(problem__id = id)
    context = {
        'submissions' : submissions
    }

    return render(request, 'submissions.html', context=context)
            

        

def submission(request, id):
    return HttpResponse("ok")
            


