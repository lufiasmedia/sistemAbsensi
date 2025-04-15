from django.shortcuts import render, redirect
from .forms import UserRegisterForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)  # ⬅️ PENTING!
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import redirect

#
# class CustomLoginView(LoginView):
#     template_name = 'users/login.html'
#
#     def get_success_url(self):
#         user = self.request.user
#
#         # Admin → redirect ke admin panel
#         if user.is_superuser:
#             return reverse('admin:index')
#
#         # Pengurus → redirect ke daftar kegiatan
#         if hasattr(user, 'profile') and user.profile.jabatan.lower() == 'pengurus':
#             return reverse('daftar_kegiatan')
#
#         # User biasa → redirect ke kegiatan hari ini
#         return reverse('kegiatan_hari_ini')

# users/views.py
from setting_app.models import Organisasi

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organisasi'] = Organisasi.objects.first()
        return context

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('admin:index')
        elif hasattr(user, 'profile') and user.profile.jabatan.lower() == 'pengurus':
            return reverse('daftar_kegiatan')
        return reverse('kegiatan_hari_ini')

