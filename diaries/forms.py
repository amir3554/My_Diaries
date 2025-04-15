from django import forms
from .models import Diary, Notes


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'description', 'mood']
        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Your diary title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your description',
                'rows': 5
            }),
            'mood': forms.Select(attrs={'class': 'form-select'}),
        }
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['description', 'important']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }