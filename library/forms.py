from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'is_available', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }