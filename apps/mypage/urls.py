from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "mypage"

urlpatterns = [
    path("", main, name="main"),
    path("myposts/", myposts, name="myposts"),
    path("mycomments/", mycomments, name="mycomments"),
    path("myscraps/", myscraps, name="myscraps"),

]
