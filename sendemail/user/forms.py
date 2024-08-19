from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})    )
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
# class UserLoginForm(forms.Form):
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.EmailInput(attrs={'class': 'form-control'})
#     )
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
    
from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid email or password')
        return self.cleaned_data

    def get_user(self):
        return self.user
    
    
from django import forms


class CustomForm(forms.Form):
    text_box_1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text_box_2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    dropdown_1 = forms.ChoiceField(
        choices=[('option1', 'Option 1'), ('option2', 'Option 2')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dropdown_2 = forms.ChoiceField(
        choices=[('option1', 'Option 1'), ('option2', 'Option 2')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )





#product forms 


class ProductFeedbackForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Product Name"
    )
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Your Name"
    )
    rating = forms.ChoiceField(
        choices=[(str(i), f"{i} Stars") for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Rating"
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label="Feedback"
    )
    purchase_date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-control'}),
        label="Purchase Date"
    )
    


class UploadFileForm(forms.Form):
    file = forms.FileField()

