from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import auth,messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.
def landing(request):
    return render(request, "landing/landing.html")

def main(request):
    return render(request, "landing/main.html")

#회원가입
User = get_user_model()

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        phone_num = request.POST.get('phone_num')

        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    name=name,
                    nickname=nickname,
                    phone_num=phone_num
                )
                user.save()
                messages.success(request, "회원가입이 완료되었습니다. 로그인하세요.")
                return redirect('landing:login')
            except IntegrityError as e:
                # Handle specific database errors (e.g., unique constraint violations)
                messages.error(request, f"입력칸을 다시 한번 확인해주세요")
            except Exception as e:
                # Handle general exceptions
                messages.error(request, f"알 수 없는 오류가 발생했습니다.")
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")

    return render(request, 'users/signup.html')

#회원탈퇴
@require_POST
@login_required   
def delete(request, id):
    user=User.objects.get(id=id)
    if user == request.user:
        user.delete()
        auth_logout(request)
        return redirect('landing:main')
    else:
        return redirect('landing:main')
#로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('landing:main')
        else:
            messages.error(request, '로그인 정보가 잘못되었습니다.')
            return render(request,'users/login.html',{'error':'로그인 정보가 잘못되었습니다.'})
    else:
        return render(request,'users/login.html')
#로그아웃
def logout(request):
    auth_logout(request)
    return redirect('landing:landing')

