from cProfile import label
from django import forms

class SubmissionForm(forms.Form):
    solution = forms.FileField(label="Upload Solution")
    problem_id = forms.IntegerField(label="Problem Id")