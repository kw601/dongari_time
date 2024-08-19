from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.views.decorators.http import require_POST
from apps.community.models import Club
from datetime import datetime
from django.http import JsonResponse
import json

# Create your views here.
def event_list(request):
    club_id = request.session.get("club_id")
    club = Club.objects.get(id=club_id)
    events = Event.objects.filter(club_id=club_id)
    form = EventForm()
    return render(
        request,
        "schedule/event_list.html",
        {
            "events": events,
            "club": club,
            "form":form
        },
    )

def event_create(request):
    club_id = request.session.get("club_id")
    club = get_object_or_404(Club, id=club_id)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()

            # AJAX 요청에 대해 JSON 응답 반환
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'event': {
                        'id': event.id,
                        'title': event.title,
                        'description': event.description,
                        'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                        'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S')
                    }
                })
            else:
                return redirect("schedule:event_list")
        else:
            # 폼이 유효하지 않으면 오류 응답
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        form = EventForm()

    return render(request, "schedule/create_event.html", {"form": form, "club": club})


def event_update(request):
    # request.POST를 사용하여 데이터를 가져옵니다.
    event_id = request.POST.get('id')
    event = get_object_or_404(Event, id=event_id)
    # POST 데이터와 함께 EventForm을 생성합니다.
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        event = form.save()
        return JsonResponse({
            'success': True,
            'event': {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S')
            }
        })
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
    
def event_delete(request):
    if request.method == "POST":
        event_id = json.loads(request.body).get('id')
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({'success': True})

def event_calendar(request):
    events = Event.objects.all()
    return render(request, "calendars/event_calendar.html", {"events": events})
