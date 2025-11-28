from django import forms
from .models import Contact, QuoteRequest, ProdevProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    role = forms.ChoiceField(choices=ProdevProfile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'role', 'password1', 'password2' ]

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full_name into first_name and last_name if needed
        full_name = self.cleaned_data['full_name'].strip()
        names = full_name.split(' ', 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service', 'details']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your phone number (optional)'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Describe your project or request...',
                'rows': 5
            }),
        }
