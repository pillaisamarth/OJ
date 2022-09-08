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


def executeFile(request, submissionId, submittedFile, language):
    submission = get_object_or_404(Submission, id=submissionId)
    problem = submission.problem
    problemId = problem.id
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
    print(verdict)
    submission.save()

    return submission




def createSubmission(problemId, submittedFile, language, user):
    problem = get_object_or_404(Problem, id = problemId)
    submission = Submission.objects.create_submission(problem=problem)
    submissionId = submission.id
    submission.submittedFile.save(f'{submissionId}.txt', submittedFile)
    submission.submittedFilePath=os.path.join(settings.MEDIA_ROOT, 'problems', str(problemId), 'submissions', f'{submissionId}.txt')
    submission.language = language
    submission.verdict = "Running"
    submission.user = user
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

    




