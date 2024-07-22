from django import forms
from DMZ.models import *

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_name','email']