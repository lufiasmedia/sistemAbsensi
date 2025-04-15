# setting_app/forms.py
from django import forms
from .models import Organisasi

class OrganisasiForm(forms.ModelForm):
    class Meta:
        model = Organisasi
        fields = ['nama', 'logo', 'favicon', 'alamat']
