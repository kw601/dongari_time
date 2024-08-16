from django.shortcuts import render, redirect
from .models import Scrap
from apps.community.models import Club, Comment, Post
from apps.landing.models import User, Auth_Club
from django.http import JsonResponse


# Create your views here.
def main(request):  # 메인
    if request.user.is_authenticated:
        return render(request, "mypage/main.html")
    else:
        return redirect("landing:login")

def myposts(request):  # 내가 작성한 글
    if request.user.is_authenticated:
        id = request.user.id  # 현재 사용자 pk
        club_id = request.session.get("club_id")  # 현재 접속한 동아리 pk
        posts = Post.objects.filter(
            user_id=id, club_id=club_id
        )  # 현재 접속한 동아리에서 유저가 작성한 모든 post 불러옴
        return render(request, "mypage/myposts.html", {"posts": posts})
    else:
        return redirect("landing:login")

def mycomments(request):  # 내가 작성한 댓글
    if request.user.is_authenticated:
        id = request.user.id
        club_id = request.session.get("club_id")  # 현재 접속한 동아리 pk
        all_comments = Comment.objects.filter(user_id=id)  # 내가 작성한 모든 댓글
        posts = Post.objects.filter(
            id__in=all_comments.values_list("post_id", flat=True), club_id=club_id
        ).distinct()  # 모든 게시물에서 현재 접속 중인 동아리 게시물만 가져옴(중복 제거)
        return render(request, "mypage/mycomments.html", {"posts": posts})
    else:
        return redirect("landing:login")

def myscraps(request):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")  # 현재 접속한 동아리 pk
        scrapped_posts = Post.objects.filter(scraped_by=request.user, club_id=club_id)
        return render(request, "mypage/myscraps.html", {"posts": scrapped_posts})
    else:
        return redirect("landing:login")

def manage_clubs(request):
    if request.user.is_authenticated:
        user_clubs = Auth_Club.objects.filter(user_id=request.user)
        current_club_id = request.session.get('club_id')
        
        return render(request, 'mypage/manage_clubs.html', {
            'user_clubs': user_clubs,
            'current_club_id': current_club_id
        })
    else:
        return redirect("landing:login")

def delete_club(request):
    if request.user.is_authenticated:
        club_id = request.POST.get("club_id")
        current_club_id = request.session.get('club_id')
        
        if club_id == current_club_id:
            return JsonResponse({
                'success': False,
                'message': '현재 접속한 동아리의 삭제는 불가능합니다. 다른 동아리로 이동 후 삭제해주세요.'
            })
        
        if club_id:
            try:
                Auth_Club.objects.filter(user_id=request.user, club_id=club_id).delete()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})
    else:
        return redirect("landing:login")