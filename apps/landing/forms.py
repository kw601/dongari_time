from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="아이디", widget=forms.TextInput(attrs={"class": "signup-input"})
    )
    password1 = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"class": "signup-input"})
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={"class": "signup-input"}),
    )
    name = forms.CharField(
        label="이름", widget=forms.TextInput(attrs={"class": "signup-input"})
    )
    nickname = forms.CharField(
        label="닉네임", widget=forms.TextInput(attrs={"class": "signup-input"})
    )
    phone_num = forms.CharField(
        label="전화번호", widget=forms.TextInput(attrs={"class": "signup-input"})
    )
    email = forms.EmailField(
            label="이메일", widget=forms.EmailInput(attrs={"class": "signup-input"})
        )
    
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "name",
            "nickname",
            "phone_num",
            "email",
        ]

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = [
            "username",
            "name",
            "nickname",
            "phone_num",
            "email",
        ]


#아이디찾기
from django import forms

class FindUsernameForm(forms.Form):
    name = forms.CharField(label='이름', max_length=20, required=True)