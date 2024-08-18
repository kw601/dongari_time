# Create your views here.
from apps.community.forms import ClubAuthForm
from .models import User, Auth_Club
from apps.community.models import Club
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    get_user_model,
)
from django.contrib import auth, messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import FindUsernameForm,SignupForm
from django.urls import reverse

# Create your views here.
def main(request):
    # 로그인 한 유저의 경우
    if request.user.is_authenticated:
        # 동아리 있으면
        if Auth_Club.objects.filter(user_id=request.user).exists():
            return render(request, "landing/main.html")
        # 동아리 없으면
        else:
            return render(request, "landing/main_first.html")
    # 로그인 하기 전
    else:
        return render(request, "landing/landing.html")


# 회원가입
User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            storage = messages.get_messages(request)
            storage.used = True 
            messages.success(request, "회원가입이 완료되었습니다. 로그인하세요.")
            return redirect('landing:login')
        else:
            messages.error(request, "회원가입 중 오류가 발생했습니다. 입력 정보를 확인하세요.")
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


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

#회원정보 수정
@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('landing:main')
    else:
        form=CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request, 'users/update.html',context)

#비밀번호 변경
def change_password(request):
  if request.method == "POST":
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
      return redirect('landing:login')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                if field == 'old_password' and 'incorrect' in error.lower():
                    messages.error(request, '기존 비밀번호가 올바르지 않습니다.')
                elif field == 'new_password2' and 'do not match' in error.lower():
                    messages.error(request, '새 비밀번호와 비밀번호 확인이 일치하지 않습니다.')
                else:
                        messages.error(request, error)
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'users/change_password.html',{"form": form})

def landing(request):
    return render(request, "landing/landing.html")


def club_auth(request):  # 동아리 인증 페이지
    if request.user.is_authenticated:  # 로그인된 유저만 접속 가능
        if request.method == "GET":
            return render(request, "landing/club_auth.html")

        if request.method == "POST":

            name = request.POST["auth_name"]  # 폼에서 클럽 이름 가져오기
            code = request.POST["auth_code"]  # 폼에서 인증 코드 가져오기

            try:
                club = Club.objects.get(
                    club_name=name
                )  # 클럽 이름으로 클럽 객체 가져오기
                if code == club.club_num:  # 코드가 일치하면
                    # 중복 가입 방지
                    if Auth_Club.objects.filter(user_id=request.user, club_id=club).exists():
                        messages.error(request, "이미 가입된 동아리입니다.")
                        return render(
                            request, "landing/club_auth.html", {"error" : "이미 가입된 동아리입니다."}
                        )

                    # Auth_Club 모델에 유저와 동아리 정보 저장
                    Auth_Club.objects.create(user_id=request.user, club_id=club)

                    request.user.save()
                    request.session["club_id"] = (
                        club.pk
                    )  # 세션에 동아리 고유번호 저장
                    return redirect("community:main")  # 메인 페이지로 이동
                else:
                    messages.error(
                        request, "인증 코드가 일치하지 않습니다."
                    )  # 폼에 에러 추가
                    return render(
                        request, "landing/club_auth.html", {"error" : "인증 코드가 일치하지 않습니다."}
                    )
            except Club.DoesNotExist:
                messages.error(
                    request, "해당 이름의 동아리가 존재하지 않습니다."
                )  # 폼에 에러 추가
                return render(
                    request, "landing/club_auth.html", {"error" : "해당 이름의 동아리가 존재하지 않습니다."}
                )
    else:
        return redirect("landing:login")  # 로그인 화면으로 이동

#아이디찾기

def find_username(request):
    username = None
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(name=name, email=email)
                username = user.username
                return redirect(reverse('landing:find_username_result') + f'?username={username}')
            except User.DoesNotExist:
                form.add_error(None, '해당 이름과 이메일로 사용자를 찾을 수 없습니다.')
            except User.MultipleObjectsReturned:
                form.add_error(None, '해당 이름과 이메일로 여러 사용자가 검색되었습니다.')
    else:
        form = FindUsernameForm()
    return render(request, 'users/find_username.html', {'form': form, 'username': username})

def find_username_result(request):
    username = request.GET.get('username', None)
    return render(request, 'users/find_username_result.html', {'username': username})