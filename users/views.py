from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


# def user_register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('Index')
        
#     else:
#         form = CustomUserCreationForm()
#         return render(request, 'register.html', {'form': form})
    