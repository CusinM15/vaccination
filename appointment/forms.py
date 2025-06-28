from django import forms
from .models import User
import secrets

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'dob', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.confirmation_token = secrets.token_hex(32)
        if commit:
            user.save()
        return user