from django.shortcuts import render, redirect
from apps.community.forms import ClubForm
from apps.community.models import Club
from apps.landing.models import User


# Create your views here.

def main(request):
    return render(request, "community/main.html")


def create_club(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = ClubForm()
            return render(request, "community/create_club.html", {"form": form})

        if request.method == "POST":
            form = ClubForm(request.POST)
            if form.is_valid():
                club = form.save()
                return redirect("community:main")
            else:
                return render(request, "community/create_club.html", {"form": form})
    else:
        return redirect("landing:login")

