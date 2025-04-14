from django.urls import path
from . import views

urlpatterns = [
    path('profil/', views.info_organisasi, name='info_organisasi'),
]
