from django import forms
from .models import Contact, QuoteRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'rows': 5,
                'class': 'form-control'
            }),
        }
class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["full_name", "email", "plan", "project_details"]
        widgets = {
            "plan": forms.HiddenInput()
        }
        labels = {
        "full_name": "Your Full Name",
        "email": "Email Address",
        "project_details": "Tell us about your project",
    }
        help_texts = {
            "project_details": "Provide as much detail as possible so we can prepare an accurate quote.",
    }