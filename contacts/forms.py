from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone"]
        labels = {"name": "Nama", "email": "Email", "phone": "Telepon"}
        widgets = {"phone": forms.TextInput(attrs={"type": "tel"})}
