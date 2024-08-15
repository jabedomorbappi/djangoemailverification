from django import forms
from django.contrib.auth import authenticate, get_user_model

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = [
#             'first_name',
#             'last_name',
#             'mobile_number',
#             'email',
#             'password',
#         ]

#     def clean_password2(self):
#         password = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#         if password != password2:
#             raise forms.ValidationError('Passwords do not match')
#         return password2

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('This Email already exists')
#         return email

#     def clean_password(self):
#         password = self.cleaned_data.get('password')
#         if len(password) < 5:
#             raise forms.ValidationError('Your password should have more than 5 characters')
#         return password
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'mobile_number',
            'email',
            'password',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This Email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError('Your password should have more than 5 characters')
        return password
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )