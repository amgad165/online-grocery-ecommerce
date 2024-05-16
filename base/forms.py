from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Passwort*', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Passwort bestätigen*', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'company_name', 'atu_number', 'email', 'bezirk','street_address','hausnummer','plz_zip','password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords are mismatch')
        
        return cleaned_data