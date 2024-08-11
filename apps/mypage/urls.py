from django.urls import path
from .views import *

app_name = "mypage"

urlpatterns = [
    path("", main, name="main"),
    path("myposts/", myposts, name="myposts"),
    path("mycomments/", mycomments, name="mycomments"),
    path("myscraps/", myscraps, name="myscraps"),
]
