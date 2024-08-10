from django.shortcuts import render, redirect
from apps.landing.forms import SignupForm
from apps.community.forms import ClubAuthForm
from .models import User, Auth_Club
from apps.community.models import Club


# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Create your views here.
def main(request):
    return render(request, "landing/landing.html")


# 회원가입
User = get_user_model()


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        name = request.POST.get("name")
        nickname = request.POST.get("nickname")
        phone_num = request.POST.get("phone_num")

        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    name=name,
                    nickname=nickname,
                    phone_num=phone_num,
                )
                user.save()
                messages.success(request, "회원가입이 완료되었습니다. 로그인하세요.")
                return redirect("landing:login")
            except IntegrityError as e:
                # Handle specific database errors (e.g., unique constraint violations)
                messages.error(request, f"입력칸을 다시 한번 확인해주세요")
            except Exception as e:
                # Handle general exceptions
                messages.error(request, f"알 수 없는 오류가 발생했습니다.")
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")

    return render(request, "users/signup.html")


# 회원탈퇴
@require_POST
@login_required
def delete(request, id):
    user = User.objects.get(id=id)
    if user == request.user:
        user.delete()
        auth_logout(request)
        return redirect("landing:main")
    else:
        return redirect("landing:main")


# 로그인
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("landing:main")
        else:
            messages.error(request, "로그인 정보가 잘못되었습니다.")
            return render(
                request, "users/login.html", {"error": "로그인 정보가 잘못되었습니다."}
            )
    else:
        return render(request, "users/login.html")


# 로그아웃
def logout(request):
    auth_logout(request)
    request.session.clear()  # 세션에 저장된 값 삭제
    return redirect("landing:main")


def landing(request):
    return render(request, "landing/landing.html")


def club_auth(request):  # 동아리 인증 페이지
    if request.user.is_authenticated:  # 로그인된 유저만 접속 가능
        if request.method == "GET":
            form = ClubAuthForm()
            return render(request, "landing/club_auth.html", {"form": form})

        if request.method == "POST":
            form = ClubAuthForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["club_name"]  # 폼에서 클럽 이름 가져오기
                code = form.cleaned_data["auth_code"]  # 폼에서 인증 코드 가져오기

                try:
                    club = Club.objects.get(
                        club_name=name
                    )  # 클럽 이름으로 클럽 객체 가져오기
                    if code == club.club_num:  # 코드가 일치하면
                        request.user.club_id = (
                            club  # 해당 유저의 가입된 동아리 정보에 동아리 pk값 입력
                        )

                        # 중복 가입 방지
                        if Auth_Club.objects.filter(user_id=request.user, club_id=club):
                            form.add_error(None, "이미 가입된 동아리입니다.")
                            return render(
                                request, "landing/club_auth.html", {"form": form}
                            )

                        # Auth_Club 모델에 유저와 동아리 정보 저장
                        Auth_Club.objects.create(user_id=request.user, club_id=club)

                        request.user.save()
                        request.session["club_id"] = (
                            club.pk
                        )  # 세션에 동아리 고유번호 저장
                        return redirect("community:main")  # 메인 페이지로 이동
                    else:
                        form.add_error(
                            None, "인증 코드가 일치하지 않습니다."
                        )  # 폼에 에러 추가
                except Club.DoesNotExist:
                    form.add_error(
                        None, "해당 이름의 동아리가 존재하지 않습니다."
                    )  # 폼에 에러 추가

            return render(request, "landing/club_auth.html", {"form": form})
    else:
        return redirect("landing:login")  # 로그인 화면으로 이동
