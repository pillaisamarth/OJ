from cProfile import label
from django import forms

class SubmissionForm(forms.Form):
    submission = forms.CharField(widget=forms.Textarea())
    problem_id = forms.IntegerField(label="Problem Id")