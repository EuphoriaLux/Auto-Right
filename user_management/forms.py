from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Enter a valid email address.'
        }
    )
    first_name = forms.CharField(
        required=False, 
        error_messages={
            'invalid': 'Enter a valid first name.'
        }
    )
    last_name = forms.CharField(
        required=False, 
        error_messages={
            'invalid': 'Enter a valid last name.'
        }
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please enter a password.',
            'invalid': 'Your password does not meet the requirements.'
        }
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please confirm your password.',
            'invalid': 'The two password fields didn’t match.'
        }
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid first name.'
        }
    )
    last_name = forms.CharField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid last name.'
        }
    )
    adress_street = forms.CharField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid street name.'
        }
    )
    adress_city = forms.CharField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid city name.'
        }
    )
    adress_zipcode = forms.CharField(
        required=False,
        error_messages={
            'invalid': 'Enter a valid street name.'
        }
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name','adress_street','adress_city','adress_zipcode')

class OnboardingStep1Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', ]

class OnboardingStep2Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['adress_street']

class OnboardingStep3Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = []