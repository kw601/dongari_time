from django.urls import path
from .views import *

app_name = "community"

urlpatterns = [
    path("create_club/", create_club, name="create_club"),
    path("main/", main, name="main"),
]
