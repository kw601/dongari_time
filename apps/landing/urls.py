from django.urls import path,include 
from .views import *
#from django.contrib.auth import views as auth_views
from . import views

app_name = "landing"

urlpatterns = [
    path("", main, name="main"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("delete/<int:id>/", delete, name="delete"),
    path("update/",update, name="update"),
    path('change_password/',change_password, name="change_password"),
    path("club_auth/", club_auth, name="club_auth"),

    path('find_username/', find_username, name='find_username'),
]

