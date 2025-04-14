from django.db import models
from django.contrib.auth.models import User

class Kegiatan(models.Model):
    nama = models.CharField(max_length=255)
    tanggal = models.DateField()
    dibuat_oleh = models.ForeignKey(User, on_delete=models.CASCADE)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama

class Kehadiran(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_absen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} hadir di {self.kegiatan.nama}"
