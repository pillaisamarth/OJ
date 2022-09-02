from dataclasses import field
from .models import Problem, Submission
from rest_framework import serializers
from . import constant
from .helpers import submitFile

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'difficulty', 'get_absolute_url']

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'statement', 'difficulty']

class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    submittedFile = serializers.FileField(required=True)
    language = serializers.ChoiceField(choices=constant.AVAILABLE_LANGUAGES, default='cpp')


    def create(self, validated_data):
        file = validated_data.pop('submittedFile')
        request = validated_data.pop('request')
        id = validated_data.pop('id')
        language = validated_data.pop('language')

        return submitFile(request=request, problemId=id, submittedFile=file, language=language)


