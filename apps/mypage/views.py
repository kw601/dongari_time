from django.shortcuts import render, redirect
from .models import Scrap
from apps.community.models import Club, Comment, Post
from apps.landing.models import User
# Create your views here.

def myposts(request):
    if request.user.is_authenticated:
        id = request.user.id
        club_id = request.session.get('club_id') 
        if request.method == 'GET':
            posts = Post.objects.filter(user_id = id, club_id = club_id)
            return render(request, "mypage/myposts.html", {"posts": posts})
    else:
        return redirect("landing:login")