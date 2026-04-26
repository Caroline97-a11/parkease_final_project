from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Staff



class StaffForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    class Meta:
        model = Staff
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'role',
        ]



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

            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            raise forms.ValidationError("First name must be at least 3 characters.")

        if not first_name.replace(" ", "").isalpha():
            raise forms.ValidationError("First name must contain letters only.")

        return first_name.title()


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) < 3:
            raise forms.ValidationError("Last name must be at least 3 characters.")

        if not last_name.replace(" ", "").isalpha():
            raise forms.ValidationError("Last name must contain letters only.")

        return last_name.title()


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if "@" not in email or "." not in email:
            raise forms.ValidationError("Enter a valid email address.")

        return email.lower()


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters.")

        if " " in username:
            raise forms.ValidationError("Username must not contain spaces.")

        return username.lower()


# =========================
# STAFF LOGIN FORM
# =========================
class StaffLoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )