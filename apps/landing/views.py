from django.shortcuts import render, redirect
from apps.landing.forms import SignupForm
from apps.community.forms import ClubAuthForm
from .models import User
from apps.community.models import Club


# Create your views here.
def landing(request):
    return render(request, "landing/landing.html")


def club_auth(request):  # 동아리 인증 페이지
    #if request.user.is_authenticated:  # 로그인된 유저만 접속 가능
        if request.method == "GET":
            form = ClubAuthForm()
            return render(request, "landing/club_auth.html",{"form": form})

        if request.method == "POST":
            form = ClubAuthForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["club_name"]  # 폼에서 클럽 이름 가져오기
                code = form.cleaned_data["auth_code"]  # 폼에서 인증 코드 가져오기

                try:
                    club = Club.objects.get(club_name=name)  # 클럽 이름으로 클럽 객체 가져오기
                    if code == club.club_num:  # 코드가 일치하면
                        request.user.club_id = club  # 해당 유저의 가입된 동아리 정보에 동아리 pk값 입력
                        request.user.save()
                        return redirect("community:main")  # 메인 페이지로 이동
                    else:
                        form.add_error(None, "인증 코드가 일치하지 않습니다.")  # 폼에 에러 추가
                except Club.DoesNotExist:
                    form.add_error(None, "해당 이름의 동아리가 존재하지 않습니다.")  # 폼에 에러 추가

            return render(request, "landing/club_auth.html", {"form": form})
    #else:
    #       return redirect("landing:login")  # 로그인 화면으로 이동
                