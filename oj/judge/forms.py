from cProfile import label
from django import forms
from . import constant

class SubmissionForm(forms.Form):
    submission = forms.FileField()
    language = forms.ChoiceField(choices=constant.AVAILABLE_LANGUAGES)