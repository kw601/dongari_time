from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm, BoardForm

# Create your views here.

def post_list(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    posts = Post.objects.filter(board_id=board)
    return render(request, "community/post_list.html", {"board": board, "posts": posts})

def post_detail(request, board_id, post_id):
    board = get_object_or_404(Board, id=board_id)
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post_id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.user_id = request.user
            comment.save()
            return redirect('community:post_detail', board_id=board.id, post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'community/post_detail.html', {'board': board, 'post': post, 'comments':comments, 'form':form})

#@login_required
def create_post(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        #form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.board_id = board
            post.save()

            #if 'image' in request.FILES:
                #pass
            
            return redirect('community:post_list', board_id=board.id)
    else:
        form = PostForm(initial={'anonymous': True})

    return render(request, 'community/create_post.html', {'form': form, 'board': board})

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