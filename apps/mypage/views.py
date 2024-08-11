from django.shortcuts import render, redirect
from .models import Scrap
from apps.community.models import Club, Comment, Post
from apps.landing.models import User
# Create your views here.

def myposts(request): # 내가 작성한 글
    if request.user.is_authenticated:
        id = request.user.id # 현재 사용자 pk
        club_id = request.session.get('club_id') # 현재 접속한 동아리 pk 
        posts = Post.objects.filter(user_id = id, club_id = club_id) # 현재 접속한 동아리에서 유저가 작성한 모든 post 불러옴
        return render(request, "mypage/myposts.html", {"posts": posts})
    else:
        return redirect("landing:login")
    
def mycomments(request): # 내가 작성한 댓글 
    if request.user.is_authenticated:
        id = request.user.id 
        club_id = request.session.get('club_id') # 현재 접속한 동아리 pk 
        all_comments = Comment.objects.filter(user_id=id) # 내가 작성한 모든 댓글
        posts = Post.objects.filter(
            id__in=all_comments.values_list('post_id', flat=True),
            club_id=club_id
        ).distinct() # 모든 게시물에서 현재 접속 중인 동아리 게시물만 가져옴(중복 제거)
        return render(request, "mypage/mycomments.html", {"posts": posts})
    else:
        return redirect("landing:login")

def myscraps(request): # 내가 스크랩 한 게시글
    if request.user.is_authenticated:  
        id = request.user.id 
        club_id = request.session.get('club_id') # 현재 접속한 동아리 pk 
        all_scraps = Scrap.objects.filter(user_id=id) # 사용자가 스크랩한 모든 게시글
        posts = Post.objects.filter(
            id__in=all_scraps.values_list('post_id', flat=True),
            club_id=club_id
        )
        return render(request, "mypage/myscraps.html", {"posts": posts})
    else:
        return redirect("landing:login") 
