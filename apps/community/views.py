from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm

# Create your views here.

def post_detail(request, board_id, post_id):
    board = get_object_or_404(Board, pk=board_id)
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if form.cleaned_data['anonymous']:
                comment.user = None
                comment.anonymous = True
            else:
                comment.user = request.user
                comment.anonymous = False
            comment.save()
            return redirect('post_detail', board_id=board_id, post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'community/post_detail.html', {'board': board, 'post':post, 'comments':comments, 'form':form})

@login_required
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
            
            return redirect('community/board_detail', board_id=board.id)
    else:
        form = PostForm(initial={'anonymous': True})

    return render(request, 'community/create_post.html', {'form': form, 'board': board})