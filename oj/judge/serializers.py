from dataclasses import field

# from judge.views import submission
from .models import Problem, Submission
from rest_framework import serializers
from . import constant
from .helpers import createSubmission, executeFile
from django.shortcuts import get_object_or_404

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'difficulty', 'get_absolute_url']

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'statement', 'difficulty']

class SubmissionSerializer(serializers.Serializer):
    problemId = serializers.IntegerField(required=False)
    submittedFile = serializers.FileField(required=True)
    language = serializers.ChoiceField(choices=constant.AVAILABLE_LANGUAGES, default='cpp')
    id = serializers.IntegerField(required=False, default=-1)


    def create(self, validated_data):
        file = validated_data.pop('submittedFile')
        request = validated_data.pop('request')
        problemId = validated_data.pop('problemId')
        language = validated_data.pop('language')
        id = validated_data.pop('id')


        try:
            obj = get_object_or_404(Submission, id = id)
            print(obj.submittedFile)
            print("Here !")
            return executeFile(request=request, submittedFile=file, language=language, submissionId=id)
        except:
            return createSubmission(problemId=problemId, submittedFile=file, language=language)
        


class SubmissionTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'