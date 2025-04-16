from django.shortcuts import render, redirect
from .forms import DiaryForm
from .models import Diary
from django.conf import settings


def home(request):
    return render(request, 'home.html', {'MEDIA_URL': settings.MEDIA_URL})

def index(request):
    return render(request, 'index.html')


def cteate_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Index')
    else:
        form = DiaryForm()
    return render(request, 'diary/create.html', {'form': form})