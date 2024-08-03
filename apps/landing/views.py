from django.shortcuts import render, redirect
from apps.landing.forms import SignupForm
from .models import User
from apps.community.models import Club


# Create your views here.
def landing(request):
    return render(request, "landing/landing.html")


def club_auth(request):  # 동아리 인증 페이지
    if request.user.is_authenticated:  # 로그인된 유저만 접속 가능
        if request.method == "GET":
            return render(request, "landing/club_auth.html")

        if request.method == "POST":
            user = request.user  # 로그인한 유저
            name = request.POST["club_name"]  # 인증하려는 동아리 이름
            code = request.POST["auth_code"]  # 유저가 입력한 인증 코드

            if (
                code == None
            ):  # 코드에 아무것도 입력하지 않은 경우 -> 장고에서 알아서 공백 입력 못하게 할 것 같긴 한데
                return render(request, "landing/club_auth.html")

            # 해당 동아리의 club_num(동아리 인증 코드)과 비교하면 됨
            club = Club.objects.filter(club_name=name)
            club_code = club.club_num

            if code == club_code:  # 코드가 일치하면
                user.club_id = (
                    club.club_id
                )  # 해당 유저의 가입된 동아리 정보에 동아리 pk값 입력
                user.save()
                return redirect("community:main")  # 메인 페이지로 이동
            else:
                return render(request, "landing/club_auth.html")
    else:
        return redirect("landing:login")  # 로그인 화면으로 이동
