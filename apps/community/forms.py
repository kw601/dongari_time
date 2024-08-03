from django import forms
from .models import Club


class ClubForm(forms.ModelForm):

    club_name = forms.CharField(
        label="동아리명", widget=forms.TextInput(attrs={"class": "createClub-input"})
    )
    club_intro = forms.CharField(
        label="동아리 소개", widget=forms.TextInput(attrs={"class": "createClub-input"})
    )
    club_num = forms.CharField(
        label="동아리 인증 번호",
        widget=forms.TextInput(attrs={"class": "createClub-input"}),
    )

    class Meta:
        model = Club
        fields = [
            "club_name",
            "club_intro",
            "club_num",
        ]

class ClubAuthForm(forms.ModelForm):

    club_name = forms.CharField(
        label="동아리명", widget=forms.TextInput(attrs={"class": "createClub-input"})
    )
    auth_code = forms.CharField(
        label="동아리 인증 번호",
        widget=forms.TextInput(attrs={"class": "createClub-input"}),
    )

    class Meta:
        model = Club
        fields = [
            "club_name",
            "auth_code",
        ]
