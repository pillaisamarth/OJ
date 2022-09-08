import filecmp
import math
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
from judge import serializers
from judge.serializers import SubmissionSerializer, ProblemListSerializer, ProblemDetailSerializer, SubmissionTableSerializer
from oj import settings
import docker
from django.utils.encoding import filepath_to_uri

from django.templatetags.static import static

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from . import constant
from rest_framework.pagination import PageNumberPagination

from .forms import SubmissionForm, TestCaseUploadForm


from .models import Problem, Submission, TestCase
# Create your views here.

def login(request):
    return HttpResponse("hello!")

class ProblemList(APIView):

    def get(self, request):
        problems = Problem.objects.all()
        serializer = ProblemListSerializer(problems, many=True)
        return Response(serializer.data)

class ProblemDetail(APIView):

    serializer_class = ProblemDetailSerializer

    def get(self, request, id):
        problem=get_object_or_404(Problem, id = id)
        languages = constant.AVAILABLE_LANGUAGES
        data = {
            'id': problem.id,
            'title': problem.title,
            'statement': problem.statement,
            'difficulty': problem.difficulty,
            'languages': languages
        }
        return Response(data)

class Submit(APIView):
    parser_class = (MultiPartParser,)
    
    def get(self, request):
        print(request.build_absolute_uri())
        return Response("hello")

    def post(self, request):

        print(request.data)
        
        serializer = SubmissionSerializer(data=request.data)
        print(request.build_absolute_uri())
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


def uploadTestCase(request):


    if request.method == 'GET':
        form = TestCaseUploadForm()
        context = {
            "form" : form
        }
        return render(request, 'uploadtestcase.html', context=context)

    form = TestCaseUploadForm(request.POST, request.FILES)

    if form.is_valid():

        problem_id = form.cleaned_data['problem']
        problem = get_object_or_404(Problem, id = problem_id)
        testcase = TestCase.objects.create_testcase(problem=problem)


        inputFile = form.cleaned_data['inputFile']
        outputFile = form.cleaned_data['outputFile']

#preparing the paths
        numTestCases = testcase.id
        relativeUploadPath = os.path.join('problems', problem_id, 'testcases', f'{numTestCases}')
        absoluteUploadPath = os.path.join(settings.MEDIA_ROOT, relativeUploadPath)

# Saving the input and output files
        inputFilePath = os.path.join('media', relativeUploadPath)
        outputFilePath = os.path.join('media', relativeUploadPath)
        

# Creating database instances
        testcase.inputFile.save(f'{numTestCases}.in', inputFile)
        testcase.outputFile.save(f'{numTestCases}.out', outputFile)
        testcase.inputPath = inputFilePath
        testcase.outputPath = outputFilePath
        testcase.save()
        
        return HttpResponse("TestCase Uploaded")

    return HttpResponse(request.method + "Invalid Form")
    



            
class Submissions(APIView):

    pagination_class = PageNumberPagination
    serializer_class = SubmissionTableSerializer

    def get(self, request, id):
        paginator = PageNumberPagination()
        submissions = Submission.objects.filter(problem__id = id)
        submissionCount = submissions.count()
        pageSize = paginator.page_size
        numberOfPages = math.ceil(submissionCount / pageSize)
        resultPage = paginator.paginate_queryset(queryset=submissions, request=request)
        data = [{
            'id' : submission.id,
            'title': submission.problem.title,
            'language': submission.get_language_display(),
            'submitted_at' : submission.submitted_at,
            'verdict': submission.verdict,
            'numberOfPages' : numberOfPages
        } for submission in resultPage]
        print(resultPage)
        return Response(data)
        

        

def submission(request, id):
    return HttpResponse("ok")
            


