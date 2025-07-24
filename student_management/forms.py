from django import forms
from .models import StudentDocument

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['title', 'document']
