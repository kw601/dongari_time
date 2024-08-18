from django.urls import path
from .views import *

app_name = "schedule"

urlpatterns = [
    path("event_list/'", event_list, name="event_list"),
    path("event_create/", event_create, name="event_create"),
]
