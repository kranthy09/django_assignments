from django import forms
from .models import Question

class QuestionForm(forms.Form):
    question = forms.CharField(max_length=250)
    answer = forms.CharField(max_length=250)