from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Board, Post, Comment, Club
from apps.mypage.models import Scrap
from apps.landing.models import User, Auth_Club
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm, BoardForm, ClubForm
from django.http import JsonResponse
from webpush import send_group_notification
from webpush import send_user_notification

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
                request.session["club_id"] = club.pk  # 세션에 동아리 고유번호 저장
                request.user.is_admin = True
                request.user.save()

                # Auth_Club 모델에 유저와 동아리 정보 저장
                Auth_Club.objects.create(user_id=request.user, club_id=club)

                # 기본 게시판 객체 생성
                default_boards = ["공지게시판", "자유게시판", "질문게시판"]
                for board_name in default_boards:
                    Board.objects.create(club_id=club, board_name=board_name)

                return redirect("community:main")
            else:
                return render(request, "community/create_club.html", {"form": form})
    else:
        return redirect("landing:login")


def select_club(request):
    if request.user.is_authenticated:
        # 사용자가 가입한 동아리 리스트 가져오기
        user_clubs = Auth_Club.objects.filter(user_id=request.user)

        if request.method == "POST":
            selected_club_id = request.POST.get("club_id")
            if selected_club_id:
                request.session["club_id"] = selected_club_id
                return redirect("community:main")

        return render(request, "community/select_club.html", {"user_clubs": user_clubs})
    else:
        return redirect("landing:login")


def post_list(request, board_id):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")
        board = get_object_or_404(Board, id=board_id, club_id=club_id)
        posts = Post.objects.filter(board_id=board, club_id=club_id).order_by(
            "-created_time"
        )
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

        is_liked = request.user in post.liked_by.all()

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post_id = post
                comment.user_id = request.user
                comment.save()

                # 알림을 보낼 사용자 목록
                notification_users = set()

                # 게시글 작성자에게 알림
                notification_users.add(post.user_id)

                # 부모 댓글이 있는 경우, 부모 댓글 작성자에게 알림
                if comment.parent_id:
                    notification_users.add(comment.parent_id.user_id)

                    # 부모 댓글에 달린 자식 댓글의 작성자도 알림 대상에 추가
                    child_comments = Comment.objects.filter(parent_id=comment.parent_id)
                    for child_comment in child_comments:
                        notification_users.add(child_comment.user_id)

                # 알림 보내기
                payload = {
                    "head": f"\"{post.title}\"에 새로운 댓글이 달렸습니다.",
                    "body": f"{comment.content[:10]}",
                }

                # 디버그용
                print(notification_users)

                for user in notification_users:
                    if user != request.user:  # 자신에게는 알림을 보내지 않음
                        send_user_notification(user=user, payload=payload, ttl=1000)

                # 그룹 알림 필요할때 사용
                # send_group_notification(
                #     group_name=notification_users, payload=payload, ttl=1000
                # )

                return redirect(
                    "community:post_detail", board_id=board.id, post_id=post.id
                )
        else:
            form = CommentForm()

        return render(
            request,
            "community/post_detail.html",
            {"board": board, "post": post, "comments": comments, "form": form, "is_liked": is_liked, "likes_count": post.liked_by.count()},
        )
    else:
        return redirect("landing:login")
    
# @login_required
def create_post(request, board_id):
    if request.user.is_authenticated:

        board = get_object_or_404(Board, pk=board_id)
        club_id = request.session.get("club_id")
        club = Club.objects.get(id=club_id)
        if request.method == "POST":
            form = PostForm(request.POST)
            # form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_id = request.user
                post.club_id = club
                post.board_id = board
                post.save()

                # if 'image' in request.FILES:
                # pass

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
                board = form.save(commit=False)
                club_id = request.session.get("club_id")
                # 같은 동아리 내에서 게시판 이름 중복 방지
                if Board.objects.filter(board_name=board.board_name, club_id=club_id):
                    form.add_error(None, "이미 존재하는 게시판 이름입니다.")
                    return render(
                        request, "community/create_board.html", {"form": form}
                    )
                else:
                    board.club_id = Club.objects.get(id=club_id)
                    board.save()
                    return redirect("community:main")
        else:
            form = BoardForm()
        return render(request, "community/create_board.html", {"form": form})
    else:
        return redirect("landing:login")


def main(request):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")
        club = Club.objects.get(id=club_id)
        boards = Board.objects.filter(club_id=club_id)
        return render(
            request,
            "community/main.html",
            {"boards": boards, "club_name": club},
        )
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


def scrap_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        scrap, created = Scrap.objects.get_or_create(user_id=request.user, post_id=post)

        if not created:
            scrap.delete()
            is_scraped = False
        else:
            is_scraped = True

        scrap_count = post.scraps.count()
        return JsonResponse({"is_scraped": is_scraped, "scrap_count": scrap_count})
    else:
        return redirect("landing:login")


def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        is_liked = False
        if user in post.liked_by.all():
            post.liked_by.remove(user)
        else:
            post.liked_by.add(user)
            is_liked = True
        post.liked = post.liked_by.count()
        post.save()
        return JsonResponse({"likes": post.liked, "is_liked": is_liked})
    else:
        return redirect("landing:login")
