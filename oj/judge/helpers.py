import os
from urllib.parse import urljoin
import docker
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Problem, Submission, TestCase
from oj import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.utils.encoding import filepath_to_uri

# def submitFile(problemId, language, submittedFile):


# # getting the problem and form details
#     problem = get_object_or_404(Problem, id = problemId)
    
# # Taking file input and saving it in filesystem as txt file.
#     numSubmittedFiles = Submission.objects.all().count()
#     relativePath = os.path.join('problems', str(problemId), 'submissions', submittedFile.name)
#     absolutePath = os.path.join(settings.MEDIA_ROOT, relativePath)
#     fs = FileSystemStorage()
#     fs.save(relativePath, submittedFile)

# # Saving the submission in the database
#     submission = Submission(problem=problem, verdict='None', language=language, submittedFile=submittedFile, submittedFilePath=absolutePath)
#     submission.save()

# # Preparing the work-area
#     workArea = os.path.join(settings.MEDIA_ROOT, 'problems', str(problemId), str(numSubmittedFiles + 1))
#     codeFile = os.path.join(workArea, submittedFile.name)
#     os.mkdir(workArea)
#     fs.save(codeFile, submittedFile)


# # Prepare testcase file - This containes the url of all testcases
#     numtestCases = problem.testcase_set.all().count()
#     inputUrlFilePath = os.path.join(workArea, 'input.txt')
    
#     testCaseBaseUrl = f'http://192.168.29.36:8000/media/problems/{str(problemId)}/testcases'

#     with open(inputUrlFilePath, 'w', newline='\n') as f:
#         for num in range(numtestCases):
#             num += 1
#             testCaseAbsoluteUrl = f'{testCaseBaseUrl}/{num}/{num}' 
#             f.write(testCaseAbsoluteUrl)
#             f.write("\n")

#     submittedFileWithoutExtension = os.path.splitext(submittedFile.name)[0]

#     verdict = "None"

# # Spawning docker containers and run codes
#     if language == 'cpp':
#         client = docker.from_env()
#         container = client.containers.run('cpmaker', 
#         f'iter.sh {submittedFile.name} input.txt', 
#         remove=True,
#         volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
#         verdict = container
#     elif language == 'java':
#         client = docker.from_env()
#         container = client.containers.run('javamaker', 
#         f'iter.sh {submittedFileWithoutExtension} input.txt', 
#         remove = True,
#         volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
#         verdict = container
#     else:
#         client = docker.from_env()
#         container = client.containers.run('pythonmaker',
#         f'iter.sh {submittedFile.name} input.txt',
#         remove = True,
#         volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
#         verdict = container
    
#     print(verdict)

# # updating the verdict of the submission in the database
    
#     verdict = verdict.decode('utf-8')
#     verdict = verdict.replace('\n', '')
#     submission.verdict = verdict
#     submission.save()

#     return submission


def submitFile(request, problemId, submittedFile, language):
    problem = get_object_or_404(Problem, id = problemId)
    submission = Submission.objects.create_submission(problem=problem)
    submissionId = submission.id
    submission.submittedFile.save(f'{submissionId}.txt', submittedFile)
    submission.submittedFilePath=os.path.join(settings.MEDIA_ROOT, 'problems', str(problemId), 'submissions', f'{submissionId}.txt')
    submission.language = language
    submission.verdict = None
    submission.save()
    testcases = problem.testcase_set.all()


# Preparing the work-area
    fs = FileSystemStorage()
    workArea = os.path.join(settings.MEDIA_ROOT, 'problems', str(problemId), str(submissionId))
    codeFile = os.path.join(workArea, submittedFile.name)
    os.mkdir(workArea)
    fs.save(codeFile, submittedFile)
    inputUrlFilePath = os.path.join(workArea, 'input.txt')

    with open(inputUrlFilePath, 'w', newline='\n') as f:
        for testcase in testcases:
            inputFilePath = testcase.inputPath
            relativeUrl = filepath_to_uri(inputFilePath)
            absoluteUrl = request.build_absolute_uri(f'/{relativeUrl}/{testcase.id}')
            f.write(absoluteUrl)
            print(f"absoluteUrl = {absoluteUrl}")
            f.write('\n')

    verdict = handleSubmission(workArea=workArea, filename=submittedFile.name,language=language)
    submission.verdict = verdict
    submission.save()

    return submission


def handleSubmission(workArea, filename, language):
    filenameWithoutExtension = os.path.splitext(filename)[0]

    if language == 'cpp':
        client = docker.from_env()
        container = client.containers.run('cpmaker', 
        f'iter.sh {filename} input.txt', 
        remove=True,
        volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
        verdict = container
    elif language == 'java':
        client = docker.from_env()
        container = client.containers.run('javamaker', 
        f'iter.sh {filenameWithoutExtension} input.txt', 
        remove = True,
        volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
        verdict = container
    else:
        client = docker.from_env()
        container = client.containers.run('pythonmaker',
        f'iter.sh {filename} input.txt',
        remove = True,
        volumes=[f'{workArea}:/mnt/vl1'], working_dir='/mnt/vl1')
        verdict = container

    verdict = verdict.decode('utf-8')
    verdict = verdict.replace('\n', '')

    return verdict

    




