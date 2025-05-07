from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from .forms import DiaryForm, DiaryUpdateForm, NotesForm
from .models import Diary, Notes
from users.models import CustomUser
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView ,CreateView, DetailView, ListView, FormView, DeleteView, UpdateView
from django.db.models import Q
import json
import random
from datetime import date


def home(request):
    return render(request, 'home.html', {'MEDIA_URL': settings.MEDIA_URL})


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        min_mood = 6
        diaries = Diary.objects.filter(user=user, mood__lte=min_mood)
        random_diaries = random.sample(list(diaries), min(len(diaries), 5))
        context['slides'] = random_diaries

        return context
    

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
        query = self.request.GET.get('query', '').strip()
        day = self.request.GET.get('day')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        filters = Q()
        if query:
            filters = Q(title__icontains=query) |  Q(description__icontains=query)

        if year and month and day:
            try:
                search_date = date(int(year), int(month), int(day))
                filters &= Q(created_at__date=search_date)
            except:
                pass
        
        return Diary.objects.filter(user=self.request.user).filter(filters).order_by('-updated_at')
    

class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = 'diary/update.html'
    pk_url_kwarg = 'diary_id'

    def test_func(self):
        return (self.request.user == self.get_object().user) # type: ignore[attr-defined]

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('UpdateDiary', args=[self.object.id])


@login_required
@require_http_methods(['DELETE'])
def delete_diary(request, pk):

    diary = get_object_or_404(Diary, id=pk)
    if request.user != diary.user:
        return JsonResponse({'message': 'Forbidden.'}, status=403)
    diary.delete()
    return JsonResponse({'message': 'diary deleted successfully.'}, status=204)
        

    
    

@login_required
@require_http_methods(['POST'])
def create_note(request, diary_id):

    diary = get_object_or_404(Diary, id=diary_id)
    if diary.user != request.user:
        return JsonResponse({'message': 'Forbidden.'}, status=403)
    
    data = json.loads(request.body)
    content = data.get("content", "")
    diary = Diary.objects.get(id=diary_id)
    note = Notes.objects.create(content=content, diary=diary)
    return JsonResponse({
        "success": True,
        'note': {
            'id': note.pk,
            'content': note.content
        }
    })


@login_required
@require_http_methods(['POST'])
def edit_note(request, diary_id, note_id):

    diary = get_object_or_404(Diary, id=diary_id)
    if request.user != diary.user:
        return JsonResponse({'message': 'Forbidden.'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    
    content = data.get("content")
    if content is None:
        return JsonResponse({'message': 'Content is required'}, status=400)
    
    note = get_object_or_404(Notes, id=note_id, diary=diary)
    note.content = content
    note.save()
    return JsonResponse({"message": "Note Edited successfully!."}, status=200)


@login_required
@require_http_methods(['DELETE'])
def delete_note(request, diary_id, note_id):

    diary = get_object_or_404(Diary, id=diary_id)
    if diary.user != request.user:
        return JsonResponse({'message': 'Forbidden.'}, status=403)
    
    note = get_object_or_404(Notes, diary=diary, pk=note_id)
    note.delete()        
    return JsonResponse({'message': 'note deleted successfully.'}, status=204)
