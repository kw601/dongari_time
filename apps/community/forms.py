from django import forms
from .models import Comment, Post, Board, Club


class CommentForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, initial=True, label="익명으로 댓글 작성"
    )
    parent_id = forms.ModelChoiceField(
        queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = Comment
        fields = ["content", "anonymous", "parent_id"]
        labels = {
            "content": "",
            "anonymous": "",
        }


class PostForm(forms.ModelForm):
    image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Post
        fields = ["title", "content", "anonymous", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "anonymous": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ("board_name",)
        labels = {
            "board_name": "게시판 이름",
        }


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
