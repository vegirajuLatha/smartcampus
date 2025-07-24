from django import forms
from .models import Complaint,Penalty,Visitor

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields =  ['subject', 'description']

class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['student', 'reason', 'amount']

from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['student', 'name', 'relation', 'purpose', 'visit_time']




