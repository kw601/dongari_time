from django.urls import path
from .views import *

app_name = "landing"

urlpatterns = [
    path("", landing, name="landing"),
]
