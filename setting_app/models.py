from django.db import models

class Organisasi(models.Model):
    nama = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo/')
    favicon = models.ImageField(upload_to='favicon/')
    alamat = models.TextField()

    def __str__(self):
        return self.nama
