from django import forms
from .models import Contact, QuoteRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name','class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address','class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject','class': 'form-control'}),
            'message': forms.Textarea(attrs={ 'placeholder': 'Your Message','rows': 5, }),
        }
class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["full_name", "email", "phone", "plan", "project_details"]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your name here', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email here', 'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'placeholder': 'Enter your number here', 'class': 'form-control'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'project_details': forms.Textarea(attrs={'placeholder': 'Add your project details here', 'rows': 6, 'class': 'form-control'}),
        }
    
        labels = {
        "full_name": "Your Full Name",
        "email": "Email Address",
        "project_details": "Project Details",
    }
        help_texts = {
            "project_details": "Provide as much detail as possible so we can prepare an accurate quote.",
    }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].required = True
        self.fields['plan'].choices = [('', 'Select a plan')] + list(self.fields['plan'].choices)