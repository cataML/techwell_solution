from django import forms
from .models import ContactMessage, BookNow, DigitalProfile,  ClientProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm

class ContactUs(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your  email', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter your subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Enter your message', 'rows': 5, 'class': 'form-control'}),
        }



class BookingNow(forms.ModelForm):
    class Meta:
        model = BookNow
        fields = ["name", "email", "contact", "service", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter your full name"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email address"
            }),
            "contact": forms.TextInput(attrs={
                "placeholder": "Enter your phone number"
            }),
            "service": forms.Select(attrs={
                "placeholder": "Select a service"
            }),
           
             "notes": forms.Textarea(attrs={
                "placeholder": "Specify your service here"
            }),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['service'].choices = [('', 'Select a service')] + list(self.fields['service'].choices)
            

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    role = forms.ChoiceField(
        choices=DigitalProfile. ROLE_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Select Service'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
          
            DigitalProfile.objects.create(
                user=user,
                full_name=self.cleaned_data["full_name"],
                phone_number =self.cleaned_data["phone"]
            )
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'bio', 'profile_picture']