from cProfile import label
from django import forms
from . import constant
from judge.models import  Problem

AVAILABLE_PROBLEMS = (
    (problem.id, problem.title) for problem in Problem.objects.all()
)

class SubmissionForm(forms.Form):
    submission = forms.FileField()
    language = forms.ChoiceField(choices=constant.AVAILABLE_LANGUAGES)


class TestCaseUploadForm(forms.Form):
    problem = forms.ChoiceField(choices=AVAILABLE_PROBLEMS)
    inputFile = forms.FileField()
    outputFile = forms.FileField()