from dataclasses import field
from .models import Problem, Submission
from rest_framework import serializers

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'difficulty', 'get_absolute_url']

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['pk', 'title', 'statement', 'difficulty']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
