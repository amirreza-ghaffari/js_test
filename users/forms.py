from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Member

user = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter Your Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter Your Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    class Meta:
        model = user
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', )


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = user
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = user
        fields = ('email',)


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = user
        fields = ('first_name', 'last_name', 'mobile_number', 'profile_image')


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'