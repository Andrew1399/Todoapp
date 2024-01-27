from django import forms
from todoapp.models import TodoList


class CreateUpdateTaskForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title', 'content', 'completed', 'desired_time']
        labels = {'title': 'Name task'}
        widgets = {'description': forms.Textarea(attrs={'cols': 70})}
