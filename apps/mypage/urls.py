from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

app_name = "mypage"

urlpatterns = [
    path("", main, name="main"),
    path("myposts/", myposts, name="myposts"),
    path("mycomments/", mycomments, name="mycomments"),
    path("myscraps/", myscraps, name="myscraps"),
    path('manage-clubs/', views.manage_clubs, name='manage_clubs'),
    path('delete-club/', views.delete_club, name='delete_club'),
    path('switch_club/<int:club_id>/', views.switch_club, name='switch_club'),
    
]
