from django.shortcuts import render, redirect, get_object_or_404

from setting_app.models import Organisasi
from .models import Kegiatan, Kehadiran
from django.contrib.auth.decorators import login_required

@login_required
def daftar_kegiatan(request):
    kegiatan_list = Kegiatan.objects.all()
    return render(request, 'absensi/daftar_kegiatan.html', {'kegiatan': kegiatan_list})

# @login_required
# def buat_kegiatan(request):
#     if request.method == 'POST':
#         nama = request.POST['nama']
#         tanggal = request.POST['tanggal']
#         keterangan = request.POST['keterangan']
#         Kegiatan.objects.create(nama=nama, tanggal=tanggal, keterangan=keterangan, dibuat_oleh=request.user)
#         return redirect('daftar_kegiatan')
#     return render(request, 'absensi/buat_kegiatan.html')

from django.contrib.auth.decorators import login_required, user_passes_test

def is_pengurus_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.jabatan.lower() == 'pengurus')


@login_required
@user_passes_test(is_pengurus_or_admin)
def buat_kegiatan(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        tanggal = request.POST['tanggal']
        keterangan = request.POST['keterangan']
        Kegiatan.objects.create(nama=nama, tanggal=tanggal, keterangan=keterangan, dibuat_oleh=request.user)
        return redirect('daftar_kegiatan')
    return render(request, 'absensi/buat_kegiatan.html')

# @login_required
# def absen_kegiatan(request, kegiatan_id):
#     kegiatan = get_object_or_404(Kegiatan, id=kegiatan_id)
#     if not Kehadiran.objects.filter(kegiatan=kegiatan, user=request.user).exists():
#         Kehadiran.objects.create(kegiatan=kegiatan, user=request.user)
#     return redirect('daftar_kegiatan')

@login_required
def absen_kegiatan(request, kegiatan_id):
    kegiatan = get_object_or_404(Kegiatan, id=kegiatan_id)
    # Cegah absen ganda
    if not Kehadiran.objects.filter(kegiatan=kegiatan, user=request.user).exists():
        Kehadiran.objects.create(kegiatan=kegiatan, user=request.user)
    return redirect('kegiatan_hari_ini')



@login_required
@user_passes_test(is_pengurus_or_admin)
def daftar_kehadiran(request, kegiatan_id):
    kegiatan = get_object_or_404(Kegiatan, id=kegiatan_id)
    daftar = Kehadiran.objects.filter(kegiatan=kegiatan)
    return render(request, 'absensi/daftar_kehadiran.html', {'kegiatan': kegiatan, 'daftar': daftar})


@login_required
def kehadiran_saya(request):
    hadir = Kehadiran.objects.filter(user=request.user).select_related('kegiatan')
    return render(request, 'absensi/kehadiran_saya.html', {'hadir': hadir})


from django.utils.timezone import now
from datetime import date

@login_required
def kegiatan_hari_ini(request):
    today = date.today()
    kegiatan_list = Kegiatan.objects.filter(tanggal=today)
    absen_list = Kehadiran.objects.filter(user=request.user, kegiatan__tanggal=today)

    # Kegiatan yang sudah diabsen oleh user hari ini
    sudah_absen_ids = absen_list.values_list('kegiatan_id', flat=True)

    organisasi = Organisasi.objects.first()

    return render(request, 'absensi/kegiatan_hari_ini.html', {
        'kegiatan_list': kegiatan_list,
        'sudah_absen_ids': sudah_absen_ids,
        'kegiatan_list': kegiatan_list,
        'sudah_absen_ids': sudah_absen_ids,
        'organisasi': organisasi,
    })
