from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, initial=True, label='익명으로 댓글 작성')

    class Meta:
        model = Comment
        fields = ['content', 'anonymous']