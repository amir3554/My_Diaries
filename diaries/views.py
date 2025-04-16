from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import DiaryForm, DiaryUpdateForm
from .models import Diary
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, FormView, DeleteView, UpdateView



def home(request):
    return render(request, 'home.html', {'MEDIA_URL': settings.MEDIA_URL})

def index(request):
    return render(request, 'index.html')


class CreateDiaryView(CreateView, LoginRequiredMixin):
    model = Diary
    form_class = DiaryForm
    template_name = 'create.html'
    success_url = reverse_lazy('DiariesList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class DiariesListView(ListView, LoginRequiredMixin):
    model = Diary
    template_name = 'diaries_list.html'
    paginate_by = 6

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
    template_name = 'update.html'
    success_url = reverse_lazy('diaries_list')

    def test_func(self):
        return (self.request.user.id == self.get_object().user_id)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('update_diary', args=[self.object.id])
    


@require_http_methods(['DELETE'])
def delete_diary(request, diary_id):
    try:
        diary = Diary.objects.get(id=diary_id)
        diary.delete()
        return JsonResponse({'message': 'diary deleted successfully.'}, status=204)
    except diary.DoesNotExist:
        return JsonResponse({'message': 'diary not found.'}, status=404)
    

