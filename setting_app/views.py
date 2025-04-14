from django.shortcuts import render
from .models import Organisasi

def info_organisasi(request):
    organisasi = Organisasi.objects.first()
    return render(request, 'setting_app/info.html', {'organisasi': organisasi})
