import filecmp
from socket import timeout
import sys
from urllib.parse import urljoin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import subprocess
import os
from django.core.files.storage import FileSystemStorage
from oj import settings
import docker
from django.utils.encoding import filepath_to_uri

from django.templatetags.static import static


from .forms import SubmissionForm, TestCaseUploadForm


from .models import Problem, Submission, TestCase
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


# def submit(request):

#     if not request.user.is_authenticated:
#         next = request.META.get('HTTP_REFERER')
#         return redirect('%s?next=%s'%(settings.LOGIN_URL, next))


    
#     form = SubmissionForm(request.POST, request.FILES)
#     folder = os.path.join(settings.FILE_PATH_FIELD_DIR, 'submissions')


    

#     if form.is_valid():
#         count = Submission.objects.all().count()
#         filefolder = os.path.join(folder, str(count + 1))
#         if os.path.isdir(filefolder)==False:
#             os.mkdir(filefolder)

#         submission = form.cleaned_data["submission"]
#         fs = FileSystemStorage(location=filefolder)
#         filename_with_extension = fs.save(name=submission.name, content = submission)
#         filename = os.path.splitext(filename_with_extension)[0]


#         problem_id = request.POST.get("problem_id")
#         problem = get_object_or_404(Problem, id = problem_id)
#         language = form.cleaned_data["language"]
        
#         # if language == 'java':
#         #     path = os.path.join(filefolder, filename)
#         #     subprocess.run(["cmd", "/c", f"javac {path}.java"])

#         testcases = problem.testcase_set.all()

#         verdict="AC"


#         #autoremove caused problems in running python scripts in containers
#         #replaced autoremove with remove

#         for testcase in testcases:
#             input = open(testcase.input, 'r')
#             inpath = os.path.join(filefolder, 'input.txt')
#             inp = open(inpath, 'w')
#             for line in input:
#                 inp.write(line)

#             inp.close()
        

#             if language == 'cpp':
#                 client = docker.from_env()
#                 container = client.containers.run('cpmaker',
#                  f'cpp_ex.sh {filename_with_extension} input.txt',
#                  remove=True,
#                  volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')
#             elif language == 'java':
#                 client = docker.from_env()
#                 container = client.containers.run('javamaker',
#                  f'java_ex.sh {filename} input.txt',
#                  remove=True,
#                  volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1')
#             else :
#                 client = docker.from_env()
#                 container = client.containers.run('pythonmaker',
#                  f'python_ex.sh {filename_with_extension} input.txt',
#                  remove=True,
#                  volumes=[f'{filefolder}:/mnt/vol1'], working_dir='/mnt/vol1',
#                  )


                 

#             # files written using notepad when read as binary 'rb' in 
#             # python contains \r\n in place of \n which adds to the total
#             # size of the file and thus the filecmp fails(it processes them
#             # as binary files). We will temporarily convert our out.txt file
#             # to replace every \n instances with \r\n instances
#             # However a better way is to replace every instance of '\r'
#             # with '' in the op1.txt file (output file stored in server)

            

#             outputpath = os.path.join(filefolder, 'out.txt') # getting filename of the file outputted by container
#             outputfile = open(outputpath, 'rb') #getting the file
#             output = outputfile.read() #getting the file cotents
#             outputfile.close() 
#             output = output.replace(b'\n', bytes('\r\n', 'utf-8')) # replacing every instance of \n with \r\n. Replace bytes with bytes
#             outputfile = open(outputpath, 'wb') #writing the revised content back to the file
#             outputfile.write(output)
#             outputfile.close()
            
            
#             if  filecmp.cmp(outputpath, testcase.output) == False:
#                 verdict = "WA"
#                 break

        
#         path = os.path.join(filefolder, filename_with_extension)
#         submission=Submission(problem = problem, verdict = verdict, language = language, submission = path)
#         submission.save()

#     return HttpResponseRedirect(reverse('submissions', args=[str(problem_id)]))

def submitFile(request):

    form = SubmissionForm(request.POST, request.FILES)

    if form.is_valid():

# getting the problem and form details
        problem_id = request.POST.get("problem_id")
        problem = get_object_or_404(Problem, id = problem_id)
        language = form.cleaned_data["language"]

# Taking file input and saving it in filesystem as txt file.
        submittedFile = form.cleaned_data["submission"]
        numSubmittedFiles = Submission.objects.all().count()
        relativePath = os.path.join('problems', problem_id, 'submissions', f'{str(numSubmittedFiles + 1)}.txt')
        absolutePath = os.path.join(settings.MEDIA_ROOT, relativePath)
        fs = FileSystemStorage()
        fs.save(relativePath, submittedFile)
        print(filepath_to_uri(relativePath))
        u = urljoin(fs.base_url, filepath_to_uri(relativePath))
        print(u)

# Saving the submission in the database
        submission = Submission(problem=problem, verdict='None', language=language, submittedFilePath=absolutePath)
        submission.save()

# Preparing the work-area
        workArea = os.path.join(settings.MEDIA_ROOT, 'problems', problem_id, str(numSubmittedFiles + 1))
        codeFile = os.path.join(workArea, submittedFile.name)
        os.mkdir(workArea)
        fs.save(codeFile, submittedFile)


# Prepare testcase file - This containes the url of all testcases
        numtestCases = problem.testcase_set.all().count()
        inputUrlFilePath = os.path.join(workArea, 'input.txt')
        
        testCaseBaseUrl = f'http://192.168.29.36:8000/media/problems/{problem_id}/testcases'

        with open(inputUrlFilePath, 'w', newline='\n') as f:
            for num in range(numtestCases):
                num += 1
                testCaseAbsoluteUrl = f'{testCaseBaseUrl}/{num}/{num}' 
                f.write(testCaseAbsoluteUrl)
                f.write("\n")

        submittedFileWithoutExtension = os.path.splitext(submittedFile.name)[0]

        verdict = "None"

# Spawning docker containers and run codes
        if language == 'cpp':
            client = docker.from_env()
            container = client.containers.run('cpmaker', 
            f'iter.sh {submittedFile.name} input.txt', 
            remove=True,
            volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
            verdict = container
        elif language == 'java':
            client = docker.from_env()
            container = client.containers.run('javamaker', 
            f'iter.sh {submittedFileWithoutExtension} input.txt', 
            remove = True,
            volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
            verdict = container
        else:
            client = docker.from_env()
            container = client.containers.run('pythonmaker',
            f'iter.sh {submittedFile.name} input.txt',
            remove = True,
            volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
            verdict = container
        
        print(verdict)

# updating the verdict of the submission in the database
        
        verdict = verdict.decode('utf-8')
        verdict = verdict.replace('\n', '')
        submission.verdict = verdict
        submission.save()

        return HttpResponseRedirect(reverse('submissions', args=[str(problem_id)]))

    return HttpResponse("No File given")
    

    

    
        

        



def uploadTestCase(request):


    if request.method == 'GET':
        form = TestCaseUploadForm()
        context = {
            "form" : form
        }
        return render(request, 'uploadtestcase.html', context=context)

    form = TestCaseUploadForm(request.POST, request.FILES)

    if form.is_valid():

# Retrieving the form inputs
        problem_id = form.cleaned_data['problem']
        problem = get_object_or_404(Problem, id = problem_id)
        inputFile = form.cleaned_data['inputFile']
        outputFile = form.cleaned_data['outputFile']

#preparing the paths
        numTestCases = problem.testcase_set.all().count()
        relativeUploadPath = os.path.join('problems', problem_id, 'testcases', f'{numTestCases + 1}')
        absoluteUploadPath = os.path.join(settings.MEDIA_ROOT, relativeUploadPath)

# Saving the input and output files
        fs = FileSystemStorage()
        inputFilePath = os.path.join(absoluteUploadPath, f'{numTestCases + 1}.in')
        outputFilePath = os.path.join(absoluteUploadPath, f'{numTestCases + 1}.out')
        fs.save(inputFilePath, inputFile)
        fs.save(outputFilePath, outputFile)

# Creating database instances
        testcase = TestCase(problem = problem, inputPath = inputFilePath, outputPath=outputFilePath)
        testcase.save()
        
        return HttpResponse("TestCase Uploaded")

    return HttpResponse(request.method + "Invalid Form")
    



def submissions(request, id):
    
    submissions = Submission.objects.filter(problem__id = id)
    context = {
        'submissions' : submissions
    }

    return render(request, 'submissions.html', context=context)
            

        

def submission(request, id):
    return HttpResponse("ok")
            


