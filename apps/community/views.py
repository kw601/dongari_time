from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post, Comment, Club
from apps.landing.models import User
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm, BoardForm, ClubForm

# Create your views here.


def create_club(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = ClubForm()
            return render(request, "community/create_club.html", {"form": form})

        if request.method == "POST":
            form = ClubForm(request.POST)
            if form.is_valid():
                club = form.save()
                return redirect("community:main")
            else:
                return render(request, "community/create_club.html", {"form": form})
    else:
        return redirect("landing:login")


def post_list(request, board_id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=board_id)
        posts = Post.objects.filter(board_id=board)
        return render(
            request, "community/post_list.html", {"board": board, "posts": posts}
        )
    else:
        return redirect("landing:login")


def post_detail(request, board_id, post_id):
    if request.user.is_authenticated:

        board = get_object_or_404(Board, id=board_id)
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post_id=post_id)

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post_id = post
                comment.user_id = request.user
                comment.save()
                return redirect(
                    "community:post_detail", board_id=board.id, post_id=post.id
                )
        else:
            form = CommentForm()

        return render(
            request,
            "community/post_detail.html",
            {"board": board, "post": post, "comments": comments, "form": form},
        )
    else:
        return redirect("landing:login")


# @login_required
def create_post(request, board_id):
    if request.user.is_authenticated:

        board = get_object_or_404(Board, pk=board_id)

        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_id = request.user
                post.board_id = board
                post.save()

                if 'image' in request.FILES:
                    post.image = request.FILES['image']
                    post.save()

                return redirect("community:post_list", board_id=board.id)
        else:
            form = PostForm(initial={"anonymous": True})

        return render(
            request, "community/create_post.html", {"form": form, "board": board}
        )
    else:
        return redirect("landing:login")


def create_board(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BoardForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("community:main")
        else:
            form = BoardForm()
        return render(request, "community/create_board.html", {"form": form})
    else:
        return redirect("landing:login")


def main(request):
    if request.user.is_authenticated:
        boards = Board.objects.all()
        return render(request, "community/main.html", {"boards": boards})
    else:
        return redirect("landing:login")


def delete_board(request, board_id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=board_id)
        if request.method == "POST":
            board.delete()
            return redirect("community:main")
        return render(request, "community/delete_board.html", {"board": board})
    else:
        return redirect("landing:login")
