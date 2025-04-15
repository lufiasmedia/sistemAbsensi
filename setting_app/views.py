from django.shortcuts import render
from .models import Organisasi

def info_organisasi(request):
    organisasi = Organisasi.objects.first()
    return render(request, 'setting_app/info.html', {'organisasi': organisasi})


# setting_app/views.py
from django.shortcuts import render, redirect
from .models import Organisasi
from .forms import OrganisasiForm
from django.contrib.auth.decorators import user_passes_test


# Hanya admin yang bisa akses
def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def kelola_organisasi(request):
    organisasi = Organisasi.objects.first()  # Ambil satu-satunya data
    if request.method == 'POST':
        form = OrganisasiForm(request.POST, request.FILES, instance=organisasi)
        if form.is_valid():
            form.save()
            return redirect('kelola_organisasi')
    else:
        form = OrganisasiForm(instance=organisasi)

    return render(request, 'setting_app/kelola_organisasi.html', {
        'form': form,
        'organisasi': organisasi,
    })
