from django.urls import path
from .views import *

app_name = "schedule"

urlpatterns = [
    path("event_list/", event_list, name="event_list"),
    path("event_create/", event_create, name="event_create"),
    path("event_update/", event_update, name="event_update"),
    path("event_delete/", event_delete, name="event_delete"),
]
