# forms.py

from django import forms
from .models import Board


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ("club_id", "board_name")
        labels = {
            "club_id": "동아리 선택",
            "board_name": "게시판 이름",
        }
