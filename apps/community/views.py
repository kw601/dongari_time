# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Post


def post_list(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    posts = Post.objects.filter(board_id=board)
    return render(request, "community/post_list.html", {"board": board, "posts": posts})


def post_detail(request, board_id, post_id):
    # 구현
    return


# @login_required
def create_post(request, board_id):
    # 구현
    return
