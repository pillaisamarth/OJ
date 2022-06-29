from cProfile import label
from django import forms

class SubmissionForm(forms.Form):
    solution = forms.CharField(widget=forms.widgets.Textarea)
    problem_id = forms.IntegerField(label="Problem Id")