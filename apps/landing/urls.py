from django.urls import path
from .views import *

app_name = "landing"

urlpatterns = [
    path("club_auth/", club_auth, name="club_auth"),
]
