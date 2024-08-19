from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="아이디", widget=forms.TextInput(attrs={"class": "signup-input"}),
        required=True
    )
    password1 = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"class": "signup-input"}),
        required=True
    )
    password2 = forms.CharField(
        label="비밀번호 확인",widget=forms.PasswordInput(attrs={"class": "signup-input"}),
        required=True
    )
    name = forms.CharField(
        label="이름", widget=forms.TextInput(attrs={"class": "signup-input"}),
        required=True
    )
    nickname = forms.CharField(
        label="닉네임", widget=forms.TextInput(attrs={"class": "signup-input"}),
        required=True
    )
    phone_num = forms.CharField(
        label="전화번호", widget=forms.TextInput(attrs={"class": "signup-input"}),
        required=True
    )
    email = forms.EmailField(
            label="이메일", widget=forms.EmailInput(attrs={"class": "signup-input"}),
            required=True
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
            "nickname",
            "phone_num",
            "email",
        ]
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        if User.objects.filter(phone_num=phone_num).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('이미 사용 중인 전화번호입니다.')
        return phone_num
    
#아이디찾기
from django import forms

class FindUsernameForm(forms.Form):
    name = forms.CharField(label='이름', max_length=20, required=True)
    email = forms.EmailField(label='이메일', max_length=20, required=True)