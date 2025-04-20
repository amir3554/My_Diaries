from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import DiaryForm, DiaryUpdateForm, NotesForm
from .models import Diary, Notes
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, FormView, DeleteView, UpdateView
import json


def home(request):
    return render(request, 'home.html', {'MEDIA_URL': settings.MEDIA_URL})

def index(request):
    return render(request, 'index.html')


class CreateDiaryView(LoginRequiredMixin ,CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/create.html'
    success_url = reverse_lazy('DiariesList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DiariesListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diaries_list.html'
    paginate_by = 6
    ordering = ['-updated_at']

    def get_queryset(self):
        query_set = super().get_queryset()
        where = {'user_id': self.request.user}
        q = self.request.GET.get('q', None)
        if q:
            where['title__icontains'] = q
        return query_set.filter(**where)
    

class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = 'diary/update.html'
    pk_url_kwarg = 'diary_id'

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('UpdateDiary', args=[self.object.id])



@require_http_methods(['DELETE'])
def delete_diary(request, pk):
    try:
        diary = Diary.objects.get(id=pk)
        diary.delete()
        return JsonResponse({'message': 'diary deleted successfully.'}, status=204)
    except diary.DoesNotExist:
        return JsonResponse({'message': 'diary not found.'}, status=404)
    



def create_note(request, diary_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        diary = Diary.objects.get(id=diary_id)
        note = Notes.objects.create(content=content, diary=diary)
        return JsonResponse({
            "success": True,
            'note': {
                'id': note.id,
                'content': note.content
            }
        })
    return JsonResponse({"success": False}, status=400)


def edit_note(request, diary_id, note_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        note = Notes.objects.get(id=note_id)
        note.content = content
        note.save()
        return JsonResponse({"success": True, "content": note.content})
    return JsonResponse({"success": False}, status=400)


@require_http_methods(['DELETE'])
def delete_note(request, diary_id, note_id):
    try:
        diary = Diary.objects.get(id=diary_id)
        note = Notes.objects.get(diary=diary, pk=note_id)
        note.delete()
        return JsonResponse({'message': 'note deleted successfully.'}, status=204)
    except note.DoesNotExist:
        return JsonResponse({'message': 'note not found.'}, status=404)
    except diary.DoesNotExist:
        return JsonResponse({'message': 'diary not found.'}, status=404)