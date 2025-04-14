from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_kegiatan, name='daftar_kegiatan'),
    path('buat/', views.buat_kegiatan, name='buat_kegiatan'),
    path('absen/<int:kegiatan_id>/', views.absen_kegiatan, name='absen_kegiatan'),
    path('kehadiran/<int:kegiatan_id>/', views.daftar_kehadiran, name='daftar_kehadiran'),
    path('kehadiran-saya/', views.kehadiran_saya, name='kehadiran_saya'),
    path('hari-ini/', views.kegiatan_hari_ini, name='kegiatan_hari_ini'),


]
