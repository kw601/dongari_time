from django.urls import path
from .views import *

app_name = "landing"

urlpatterns = [

    path('signup/', signup, name="signup"),
    path("", landing, name="landing"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('delete/<int:id>/', delete, name="delete"),
    path('main/', main, name="main" ),
    path("club_auth/", club_auth, name="club_auth"),
]

