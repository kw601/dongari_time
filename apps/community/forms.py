from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, initial=True, label='익명으로 댓글 작성')

    class Meta:
        model = Comment
        fields = ['content', 'anonymous']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'anonymous']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    #image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))