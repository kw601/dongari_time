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