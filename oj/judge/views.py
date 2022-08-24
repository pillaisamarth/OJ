import filecmp
from socket import timeout
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

        #autoremove caused problems in running python scripts in containers
        #replaced autoremove with remove

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
                 remove=True,
                 volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')
            elif language == 'java':
                client = docker.from_env()
                container = client.containers.run('javamaker',
                 f'java_ex.sh {filename} input.txt',
                 remove=True,
                 volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')
            else :
                client = docker.from_env()
                container = client.containers.run('pythonmaker',
                 f'python_ex.sh {filename_with_extension} input.txt',
                 remove=True,
                 volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')


                 

            # files written using notepad when read as binary 'rb' in 
            # python contains \r\n in place of \n which adds to the total
            # size of the file and thus the filecmp fails(it processes them
            # as binary files). We will temporarily convert our out.txt file
            # to replace every \n instances with \r\n instances
            # However a better way is to replace every instance of '\r'
            # with '' in the op1.txt file (output file stored in server)

            

            outputpath = os.path.join(filefolder, 'out.txt') # getting filename of the file outputted by container
            outputfile = open(outputpath, 'rb') #getting the file
            output = outputfile.read() #getting the file cotents
            outputfile.close() 
            output = output.replace(b'\n', bytes('\r\n', 'utf-8')) # replacing every instance of \n with \r\n. Replace bytes with bytes
            outputfile = open(outputpath, 'wb') #writing the revised content back to the file
            outputfile.write(output)
            outputfile.close()
            
            
            if  filecmp.cmp(outputpath, testcase.output) == False:
                verdict = "WA"
                break

        
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
            


