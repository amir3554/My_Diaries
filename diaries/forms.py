from django import forms
from .models import Diary, Notes
from django.utils.translation import gettext as trans

attrs = {'class' : 'form-control'}

class DiaryForm(forms.ModelForm):

    class Meta():

        model = Diary

        fields = ['title', 'description', 'mood']
             
        labels = {
            'title' : trans('Your diary title'),
            'description' : trans('Type here your diary, how was your day!'),
            'mood' : trans('Mood')
        }
        widgets = {
            'title' : forms.TextInput(attrs=attrs),
            'description': forms.Textarea(attrs=attrs),
            'mood': forms.Select(attrs=attrs)
        }

class DiaryUpdateForm(forms.ModelForm):

    class Meta():

        model = Diary

        fields = ['title', 'description', 'mood']
             
        labels = {
            'title' : trans('Your diary title'),
            'description' : trans('Type here your diary, how was your day!'),
            'mood' : trans('Mood')
        }
        widgets = {
            'title' : forms.TextInput(attrs=attrs),
            'description': forms.Textarea(attrs=attrs),
            'mood': forms.Select(attrs=attrs)
        }


class NotesForm(forms.ModelForm):

    class Meta():

        model = Notes

        fields = ['description', 'important']

        labels = {
            'description' : trans('Type here your diary, how was your day!'),
            'important' : trans('Important')
        }

        widgets = {
            'description': forms.TextInput(attrs=attrs),
            'important': forms.CheckboxInput(attrs=attrs)
            }