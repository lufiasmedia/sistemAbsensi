from django.urls import path
from . import views

urlpatterns = [
    path('profil/', views.info_organisasi, name='info_organisasi'),
    path('kelola/', views.kelola_organisasi, name='kelola_organisasi'),
]
