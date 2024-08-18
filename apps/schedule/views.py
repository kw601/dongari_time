from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from apps.community.models import Club
from datetime import datetime


# Create your views here.
def event_list(request):
    club_id = request.session.get("club_id")
    events = Event.objects.filter(club_id=club_id)
    return render(
        request,
        "schedule/event_list.html",
        {
            "events": events,
            "club": club_id,
        },
    )


def event_create(request):
    club_id = request.session.get("club_id")
    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club  # 이벤트를 특정 동아리에 연결
            event.save()
            return redirect("schedule:event_list", club_id=club.id)
    else:
        form = EventForm()

    return render(request, "schedule/create_event.html", {"form": form, "club": club})


def event_calendar(request):
    events = Event.objects.all()
    return render(request, "calendars/event_calendar.html", {"events": events})
