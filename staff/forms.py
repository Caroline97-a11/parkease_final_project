from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff


# =========================
# STAFF REGISTRATION FORM
# =========================
class StaffForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            'role',
        ]

        labels = {
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
            'email': 'Enter Email Address',
            'username': 'Enter Username',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
            'created_at': 'Date of Registration',
            'role': 'Select Role'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com'
            }),

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),


            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # ✅ Validate last name (only alphabets)
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise forms.ValidationError('Please enter your last name')

        if not last_name.isalpha():
            raise forms.ValidationError('Last name should contain only alphabets')

        return last_name


# =========================
# STAFF LOGIN FORM
# =========================
class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        error_messages={'required': 'This field cannot be empty!'}
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        error_messages={'required': 'Please enter your password!'}
    )