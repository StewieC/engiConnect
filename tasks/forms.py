from django import forms
from core.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'budget', 'deadline', 'attachments_note']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'w-full'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }