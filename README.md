## 📋 **Analisis Kebutuhan Sistem Manajemen Absensi IMM Kolaka Utara**

### 1. 👥 **Pengguna (User Roles):**
Sistem ini akan digunakan oleh tiga jenis pengguna, masing-masing dengan hak akses yang berbeda:

#### a. **Admin**
- Memiliki akses penuh terhadap sistem.
- Bertanggung jawab mengelola data absensi dan data pengguna.

#### b. **Anggota Organisasi**
- Pengguna umum yang melakukan absensi harian atau kehadiran dalam kegiatan.
- Dapat melihat riwayat absensinya sendiri.

#### c. **Pengurus Organisasi**
- Sama seperti anggota, namun memiliki wewenang tambahan seperti monitoring kehadiran anggota di bawah koordinasinya.
- Dapat melihat riwayat absensi seluruh anggota.

---

### 2. 🧩 **Fitur Sistem:**

#### a. **Absensi Harian**
- Digunakan oleh anggota dan pengurus untuk menandai kehadiran harian (misalnya saat masuk sekretariat atau saat kerja harian organisasi).

#### b. **Absensi Rapat/Kegiatan**
- Digunakan saat kegiatan resmi IMM seperti rapat, kajian, bakti sosial, dll.
- Setiap kegiatan dapat memiliki absensi terpisah.

#### c. **Pengelolaan Data Absensi (Admin)**
- Admin dapat:
  - Melihat seluruh data absensi.
  - Menambahkan, mengubah, dan menghapus data absensi jika terjadi kesalahan input.
  - Mengekspor laporan absensi ke dalam format Excel/PDF.

#### d. **Riwayat Absensi (Anggota & Pengurus)**
- Masing-masing pengguna dapat melihat histori absensi pribadinya.
- Pengurus dapat melihat riwayat kehadiran seluruh anggota untuk keperluan evaluasi.



Kamu benar sekali, dan terima kasih sudah mengingatkan 🙌  
Penjelasan sebelumnya memang terlalu fokus pada `users`, padahal dalam proyekmu ada **tiga app utama**:  
➡️ `users` – untuk manajemen akun dan jabatan  
➡️ `absensi` – untuk pengelolaan kegiatan dan absensi  
➡️ `setting_app` – untuk informasi organisasi  

Nah, berikut ini saya buatkan ulang **penjelasan proyek dari awal**, **lengkap untuk ketiga app**, dan disusun **step-by-step agar mudah kamu salin ke README GitHub**.

---

## 📘 SISTEM MANAJEMEN ABSENSI IMM KOLAKA UTARA – LENGKAP

### 🔰 Tujuan Proyek:
Sistem ini dirancang untuk mencatat kehadiran anggota IMM Kolaka Utara dalam kegiatan organisasi, dengan pengelolaan berdasarkan **jabatan pengguna**:
- Admin
- Pengurus
- User biasa (anggota)

---

## 🏗️ STRUKTUR APLIKASI (3 APP UTAMA)

### 1. `users`: Manajemen akun dan jabatan pengguna

- Menyimpan informasi profil user seperti:
  - Jabatan (admin / pengurus / anggota)
  - No HP
  - Foto profil
- Mengatur login & redirect berdasarkan jabatan
- Otomatis membuat profil saat user baru dibuat (dengan `signals`)
- Menggunakan Django default `User` + `Profile` tambahan

### 2. `absensi`: Kegiatan dan Kehadiran

- **Kegiatan** dibuat oleh admin/pengurus
- **Kehadiran** dicatat saat anggota mengisi absensi
- User biasa:
  - Hanya bisa melihat kegiatan **hari ini**
  - Bisa absen jika belum absen
- Pengurus/admin:
  - Bisa membuat kegiatan
  - Bisa melihat seluruh kehadiran

### 3. `setting_app`: Informasi Organisasi

- Menyimpan data umum organisasi seperti:
  - Nama organisasi
  - Logo
  - Favicon
  - Alamat sekretariat
- Ditampilkan di halaman profil publik

---

## 🔧 LANGKAH-LANGKAH MENGEMBANGKAN PROYEK

### 1. Buat Proyek Django di PyCharm Professional

```bash
django-admin startproject absensi_imm
cd absensi_imm
```

### 2. Buat Ketiga App

```bash
python manage.py startapp users
python manage.py startapp absensi
python manage.py startapp setting_app
```

### 3. Tambahkan ke `INSTALLED_APPS` di `settings.py`

```python
INSTALLED_APPS = [
    ...
    'users',
    'absensi',
    'setting_app',
]
```

---

## 📁 RINGKASAN STRUKTUR TIAP APP

### ✅ APP `users`

**models.py**
```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jabatan = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='foto/', null=True, blank=True)
```

**signals.py** – Membuat profil otomatis:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
```

**views.py** – Login kustom berdasarkan jabatan:
```python
from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('admin:index')
        elif hasattr(user, 'profile') and user.profile.jabatan.lower() == 'pengurus':
            return reverse('daftar_kegiatan')
        return reverse('kegiatan_hari_ini')
```

---

### ✅ APP `absensi`

**models.py**
```python
from django.db import models
from django.contrib.auth.models import User

class Kegiatan(models.Model):
    nama = models.CharField(max_length=255)
    tanggal = models.DateField()
    dibuat_oleh = models.ForeignKey(User, on_delete=models.CASCADE)
    keterangan = models.TextField(blank=True)

class Kehadiran(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_absen = models.DateTimeField(auto_now_add=True)
```

**views.py** – contoh fungsi penting:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Kegiatan, Kehadiran
from datetime import date

@login_required
def kegiatan_hari_ini(request):
    today = date.today()
    kegiatan_list = Kegiatan.objects.filter(tanggal=today)
    absen_list = Kehadiran.objects.filter(user=request.user, kegiatan__tanggal=today)
    sudah_absen_ids = absen_list.values_list('kegiatan_id', flat=True)

    return render(request, 'absensi/kegiatan_hari_ini.html', {
        'kegiatan_list': kegiatan_list,
        'sudah_absen_ids': sudah_absen_ids
    })

@login_required
def absen_kegiatan(request, kegiatan_id):
    kegiatan = get_object_or_404(Kegiatan, id=kegiatan_id)
    if not Kehadiran.objects.filter(kegiatan=kegiatan, user=request.user).exists():
        Kehadiran.objects.create(kegiatan=kegiatan, user=request.user)
    return redirect('kegiatan_hari_ini')
```

---

### ✅ APP `setting_app`

**models.py**
```python
from django.db import models

class Organisasi(models.Model):
    nama = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo/')
    favicon = models.ImageField(upload_to='favicon/')
    alamat = models.TextField()
```

**views.py**
```python
from django.shortcuts import render
from .models import Organisasi

def info_organisasi(request):
    organisasi = Organisasi.objects.first()
    return render(request, 'setting_app/info.html', {'organisasi': organisasi})
```

---

## 🌐 URL Routing Utama (`absensi_imm/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('kegiatan_hari_ini')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('absensi/', include('absensi.urls')),
    path('setting/', include('setting_app.urls')),
]
```

---

## ✅ Jalankan Aplikasi

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buka browser: `http://127.0.0.1:8000/`


