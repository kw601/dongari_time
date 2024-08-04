# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Post
from .forms import BoardForm


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


def create_board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("community:board_list")
    else:
        form = BoardForm()
    return render(request, "community/create_board.html", {"form": form})


def board_list(request):
    boards = Board.objects.all()
    return render(request, "community/board_list.html", {"boards": boards})


def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == "POST":
        board.delete()
        return redirect("community:board_list")
    return render(request, "community/delete_board.html", {"board": board})
