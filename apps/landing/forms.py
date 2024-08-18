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
            "username",
            "name",
            "nickname",
            "phone_num",
            "email",
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email

    # 중복된 닉네임 확인
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nickname

    # 중복된 아이디(유저네임) 확인
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용 중인 아이디입니다.")
        return username
    
    
#아이디찾기
from django import forms

class FindUsernameForm(forms.Form):
    name = forms.CharField(label='이름', max_length=20, required=True)
    email = forms.EmailField(label='이메일', max_length=20, required=True)