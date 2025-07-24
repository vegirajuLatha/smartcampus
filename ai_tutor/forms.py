# ai_tutor/forms.py

from django import forms
from attendance.models import SyllabusDocument

class SyllabusUploadForm(forms.ModelForm):
    class Meta:
        model = SyllabusDocument
        fields = ['title', 'file']
