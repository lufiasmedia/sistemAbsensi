from django import forms
from django.contrib.auth.models import User
from .models import Profile

# class UserRegisterForm(forms.ModelForm):
#     jabatan = forms.CharField(max_length=100)
#     no_hp = forms.CharField(max_length=15, required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             Profile.objects.create(
#                 user=user,
#                 jabatan=self.cleaned_data['jabatan'],
#                 no_hp=self.cleaned_data['no_hp']
#             )
#         return user

# users/forms.py

# from django import forms
# from django.contrib.auth.models import User
# from .models import Profile
#
# class UserRegisterForm(forms.ModelForm):
#     nama_lengkap = forms.CharField(max_length=150)
#     jabatan = forms.CharField(max_length=100)
#     no_hp = forms.CharField(max_length=15, required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             Profile.objects.create(
#                 user=user,
#                 nama_lengkap=self.cleaned_data['nama_lengkap'],
#                 jabatan=self.cleaned_data['jabatan'],
#                 no_hp=self.cleaned_data['no_hp']
#             )
#         return user

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    nama_lengkap = forms.CharField(max_length=150)
    jabatan = forms.CharField(max_length=100)
    no_hp = forms.CharField(max_length=15, required=False)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                nama_lengkap=self.cleaned_data['nama_lengkap'],
                jabatan=self.cleaned_data['jabatan'],
                no_hp=self.cleaned_data['no_hp'],
                foto=self.cleaned_data.get('foto')
            )
        return user


