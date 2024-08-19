from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.urls import reverse
from .models import Board, Post, Comment, Club
from apps.mypage.models import Scrap
from apps.landing.models import User, Auth_Club
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm, BoardForm, ClubForm
from django.http import JsonResponse
from webpush import send_group_notification
from webpush import send_user_notification

# Create your views here.


def create_club(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            print(request.POST)
            form = ClubForm()
            return render(request, "community/create_club.html", {"form": form})
        if request.method == "POST":
            form = ClubForm(request.POST)
            if form.is_valid():
                club = form.save()
                request.session["club_id"] = club.pk  # 세션에 동아리 고유번호 저장
                request.session["club_name"] = club.club_name  # 세션에 동아리 이름 저장
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
        club_id = request.session.get("club_id")
        boards = Board.objects.filter(club_id=club_id)
        if request.method == "POST":
            selected_club_id = request.POST.get("club_id")
            club = Club.objects.get(id=selected_club_id)
            if selected_club_id:
                request.session["club_id"] = selected_club_id
                request.session["club_name"] = club.club_name
                return redirect("community:main")

        return render(
            request,
            "community/select_club.html",
            {"user_clubs": user_clubs, "boards": boards},
        )
    else:
        return redirect("landing:login")


def post_list(request, board_id):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")
        board = get_object_or_404(Board, id=board_id, club_id=club_id)
        posts = Post.objects.filter(board_id=board, club_id=club_id).order_by(
            "-pinned", "-created_time"
        )
        form = PostForm(initial={"anonymous": True})
        boards = Board.objects.filter(club_id=club_id)
        posts_best = Post.objects.filter(club_id=club_id, liked_cnt__gte=5)
        return render(
            request,
            "community/post_list.html",
            {
                "board": board,
                "posts": posts,
                "form": form,
                "boards": boards,
                "posts_best": posts_best,
            },
        )
    else:
        return redirect("landing:login")


def post_detail(request, board_id, post_id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=board_id)
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post_id=post_id)
        club_id = request.session.get("club_id")
        boards = Board.objects.filter(club_id=club_id)
        posts_best = Post.objects.filter(club_id=club_id, liked_cnt__gte=5)

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
                # 알림 url 생성
                comment_url = request.build_absolute_uri(
                    reverse("community:post_detail", args=[board_id, post_id])
                )
                payload = {
                    "head": f'"{post.title}"에 새로운 댓글이 달렸습니다.',
                    "body": f"{comment.content[:10]}",
                    "url": comment_url,  # paload에 url 추가
                }

                # 디버그용
                print(notification_users)

                for user in notification_users:
                    if user != request.user:  # 자신에게는 알림을 보내지 않음
                        print("post detail에서 알림")
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
            {
                "board": board,
                "post": post,
                "comments": comments,
                "form": form,
                "is_liked": is_liked,
                "likes_count": post.liked_by.count(),
                "boards": boards,
                "posts_best": posts_best,
                "scrap_count": post.scraped_by.count(),
            },
        )
    else:
        return redirect("landing:login")


"""
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
"""


def create_post(request, board_id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=board_id)
        club_id = request.session.get("club_id")
        club = Club.objects.get(id=club_id)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.club_id = club
            post.board_id = board
            post.save()

            # 공지게시판에 글 작성시 공지게시판의 동아리원 전부에게 알림 전송
            if board.board_name == "공지게시판":
                # 알림을 보낼 사용자 목록
                notification_users = set()

                # Auth_Club 모델에서 글을 작성하는 공지 게시판 동아리의 소속 동아리원들을 가져옴
                club_members = Auth_Club.objects.filter(club_id=club_id)
                for club_member in club_members:
                    notification_users.add(club_member.user_id)

                # 알림 보내기
                # create_post로 인해 만들어진 post의 절대 url 생성
                post_url = request.build_absolute_uri(
                    reverse("community:post_detail", args=[board.id, post.id])
                )
                payload = {
                    "head": f"{club.club_name} 동아리에 새로운 공지사항이 등록되었습니다.",
                    "body": f"{post.title}",
                    "url": post_url,  # paload에 url 추가
                }

                # 디버그용
                print(notification_users)

                for user in notification_users:
                    if (
                        user != request.user
                    ):  # 자신에게는 알림을 보내지 않음, 알림 버튼 활성화인 유저한테만 보냄
                        send_user_notification(user=user, payload=payload, ttl=1000)

                # 그룹 알림 필요할때 사용
                # send_group_notification(
                #     group_name=notification_users, payload=payload, ttl=1000
                # )

            return JsonResponse(
                {
                    "status": "success",
                    "post_id": post.id,
                    "board_name": board.board_name,
                    "title": post.title,
                    "content": (
                        post.content[:100] + "..."
                        if len(post.content) > 100
                        else post.content
                    ),
                    "created_time": post.created_time.strftime("%Y/%m/%d"),
                    "user_name": post.user_id.name,
                    "user": post.user_id.nickname if not post.anonymous else "익명",
                    "anonymous": post.anonymous,
                    "comments_count": post.comment_set.count(),  # 댓글 수 추가
                    "likes_count": post.liked_by.count(),  # 좋아요 수 추가
                    "scraps_count": post.scraped_by.count(),  # 스크랩 수 추가
                }
            )
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        return redirect("landing:login")


def create_board(request):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")
        boards = Board.objects.filter(club_id=club_id)
        if request.method == "POST":
            form = BoardForm(request.POST)
            if form.is_valid():
                board = form.save(commit=False)
                club_id = request.session.get("club_id")
                # 같은 동아리 내에서 게시판 이름 중복 방지
                if Board.objects.filter(board_name=board.board_name, club_id=club_id):
                    form.add_error(None, "이미 존재하는 게시판 이름입니다.")
                    return render(
                        request,
                        "community/create_board.html",
                        {"form": form, "boards": boards},
                    )
                else:
                    board.club_id = Club.objects.get(id=club_id)
                    board.save()
                    return redirect("community:main")
        else:
            form = BoardForm()
        return render(
            request, "community/create_board.html", {"form": form, "boards": boards}
        )
    else:
        return redirect("landing:login")


def main(request):
    if request.user.is_authenticated:
        club_id = request.session.get("club_id")
        club = Club.objects.get(id=club_id)
        boards = Board.objects.filter(club_id=club_id)

        # 각 게시판에 대해 상위 5개의 게시글을 가져오기
        board_posts = {}
        for board in boards:
            posts = Post.objects.filter(club_id=club.id, board_id=board.id).order_by(
                "-id"
            )[:5]
            board_posts[board.id] = (
                posts  # 각 게시판의 게시글을 board_posts 딕셔너리에 저장
            )

        posts_best = Post.objects.filter(club_id=club_id, liked_cnt__gte=5)

        return render(
            request,
            "community/main.html",
            {
                "boards": boards,
                "club_name": club,
                "board_posts": board_posts,
                "posts_best": posts_best,
            },
        )
    else:
        return redirect("landing:login")


def delete_board(request, board_id):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, id=board_id)

        # 필수 게시판 3개는 삭제 불가
        restricted_boards = ["공지게시판", "질문게시판", "자유게시판"]

        if board.board_name in restricted_boards:
            messages.error(
                request,
                f"{board.board_name}은 삭제할 수 없습니다.",
            )
            return redirect("community:post_list", board_id=board_id)
        if request.method == "POST":
            board.delete()
            return redirect("community:main")
    else:
        return redirect("landing:login")


def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        board_id = post.board_id
        if request.method == "POST":
            post.delete()
            return redirect("community:post_list", board_id=board_id)
    else:
        return redirect("landing:login")


def scrap_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        scrap, created = Scrap.objects.get_or_create(user_id=request.user, post_id=post)

        if not created:
            scrap.delete()
            is_scraped = False
            post.scrap_cnt -= 1
        else:
            is_scraped = True
            post.scrap_cnt += 1

        scrap_count = post.scraps.count()
        # return JsonResponse({"is_scraped": is_scraped})
        return JsonResponse({"is_scraped": is_scraped, "scrap_count": scrap_count})
    # 스크랩 수 만약에 구현하게 되면
    else:
        return redirect("landing:login")


def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        is_liked = False
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            post.liked_cnt -= 1
        else:
            post.liked_by.add(user)
            is_liked = True
            post.liked_cnt += 1

        post.liked = post.liked_by.count()
        post.save()
        return JsonResponse({"likes": post.liked, "is_liked": is_liked})
    else:
        return redirect("landing:login")


def delete_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user_id:
            post = comment.post_id
            comment.delete()
            return redirect(
                "community:post_detail", board_id=post.board_id.id, post_id=post.id
            )
        else:
            # 작성자가 아닌 경우 처리
            return redirect(
                "community:post_detail",
                board_id=comment.post_id.board_id.id,
                post_id=comment.post_id.id,
            )
    else:
        return redirect("landing:login")


def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user_id:
            board_id = post.board_id.id
            post.delete()
            return redirect("community:post_list", board_id=board_id)
        else:
            # 작성자가 아닌 경우 처리
            return redirect(
                "community:post_detail", board_id=post.board_id.id, post_id=post.id
            )
    else:
        return redirect("landing:login")


def create_comment(request, board_id, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.post_id = post
            comment.save()

            # 알림을 보낼 사용자 목록
            notification_users = set()

            # 게시글 작성자에게 알림 위해 목록에 추가
            notification_users.add(post.user_id)

            # 부모 댓글이 있는 경우, 부모 댓글 작성자에게 알림
            if comment.parent_id:
                notification_users.add(comment.parent_id.user_id)

                # 부모 댓글에 달린 자식 댓글의 작성자도 알림 대상에 추가
                child_comments = Comment.objects.filter(parent_id=comment.parent_id)
                for child_comment in child_comments:
                    notification_users.add(child_comment.user_id)

            # debug
            print("create_comment에서 알림")
            # 알림 보내기
            # 알림 url 생성
            comment_url = request.build_absolute_uri(
                reverse("community:post_detail", args=[board_id, post_id])
            )
            payload = {
                "head": f'"{post.title}"에 새로운 댓글이 달렸습니다.',
                "body": f"{comment.content[:10]}",
                "url": comment_url,  # paload에 url 추가
            }

            # 디버그용
            print(notification_users)

            for user in notification_users:
                if (
                    user != request.user
                ):  # 자신에게는 알림을 보내지 않음, 알림 활성화인 유저한테만 보냄
                    send_user_notification(user=user, payload=payload, ttl=1000)

            # 그룹 알림 필요할때 사용
            # send_group_notification(
            #     group_name=notification_users, payload=payload, ttl=1000
            # )

            return redirect("community:post_detail", board_id=board_id, post_id=post.id)
        else:
            return JsonResponse({"error": "Form invalid"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def toggle_pinned(request, board_id, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if request.method == "POST":
            post.pinned = not post.pinned
            post.save()
            return redirect("community:post_detail", board_id=board_id, post_id=post_id)
    else:
        return redirect("landing:login")


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]  # 검색한 단어
        club_id = request.session.get("club_id")
        boards = Board.objects.filter(club_id=club_id)
        posts_best = Post.objects.filter(club_id=club_id, liked_cnt__gte=5)
        if request.POST.get("board_id"):  # 게시판 내부일 때
            board_id = request.POST.get("board_id")
            board = Board.objects.get(id=board_id)  # 게시판 정보
            posts = Post.objects.filter(
                club_id=club_id, board_id=board_id, title__contains=searched
            )  # 게시판에서 검색한 단어가 포함되는 게시글을 가져옴
            return render(
                request,
                "community/post_list.html",
                {
                    "posts": posts,
                    "board": board,
                    "boards": boards,
                    "posts_best": posts_best,
                },
            )
        else:  # 메인 화면일 때(헤더바에서 검색했을 때)
            posts = Post.objects.filter(
                club_id=club_id, title__contains=searched
            )  # 전체 게시글에서 검색한 단어가 포함되는 게시글만 가져옴
            return render(
                request,
                "community/search_list.html",
                {
                    "posts": posts,
                    "searched": searched,
                    "boards": boards,
                    "posts_best": posts_best,
                },
            )


def load_more_boards(request):
    start = int(request.GET.get("start", 0))
    limit = int(request.GET.get("limit", 4))
    club_id = request.session.get("club_id")

    # 현재 세션에 저장된 club_id를 가지는 모든 게시판 가져오기
    boards = Board.objects.filter(club_id=club_id)[start : start + limit]

    # JSON 응답에 넣을 데이터 구성
    boards_data = []
    for board in boards:
        posts = Post.objects.filter(board_id=board.id).values(
            "id", "title", "created_time"
        )
        boards_data.append(
            {"id": board.id, "name": board.board_name, "posts": list(posts)}
        )

    # 현재 클럽에 속한 전체 게시판 수 계산
    total_boards_count = Board.objects.filter(club_id=club_id).count()

    return JsonResponse(
        {"boards": boards_data, "total_boards_count": total_boards_count}
    )
