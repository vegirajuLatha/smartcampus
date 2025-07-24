from django import forms
from .models import SyllabusDocument

class SyllabusUploadForm(forms.ModelForm):
    class Meta:
        model = SyllabusDocument
        fields = ['title', 'file']
