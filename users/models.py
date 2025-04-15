from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     jabatan = models.CharField(max_length=100)
#     no_hp = models.CharField(max_length=15, blank=True)
#     foto = models.ImageField(upload_to='foto/', blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.jabatan}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=150, blank=True, null=True)  # ⬅️ Tambahkan ini
    jabatan = models.CharField(max_length=100, blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True)
    foto = models.ImageField(upload_to='foto/', blank=True, null=True)

    def __str__(self):
        return f"{self.nama_lengkap} ({self.user.username}) - {self.jabatan}"

