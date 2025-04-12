from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib.auth import authenticate, login
from django.db.models import Q


def event_list(request):
    events = Event.objects.all().order_by('date')

    keyword = request.GET.get('search')
    date = request.GET.get('date')
    location = request.GET.get('location')
    if keyword:
        events = events.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )
    if date:
        events = events.filter(date__date=date)
    if location:
        events = events.filter(location__icontains=location)

    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participation_set.filter(status='registered')
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.organizer = request.user
            new_event.save()
            form.save_m2m()
            extra_images = request.FILES.getlist('extra_images')
            for img in extra_images:
                EventExtraImage.objects.create(event=new_event, image=img)
            return redirect('event_detail', event_id=new_event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

@login_required
def participate_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participation, created = Participation.objects.get_or_create(user=request.user, event=event)
    if not created:
        if participation.status == 'registered':
            participation.status = 'canceled'
        else:
            participation.status = 'registered'
        participation.save()
    else:
        participation.status = 'registered'
        participation.save()
    return redirect('event_detail', event_id=event_id)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserRegistrationForm
    return render(request, 'account/registration.html', {'form': form})


@login_required
def my_account(request):
    user = request.user
    organized_events = Event.objects.filter(organizer=user).order_by('date')
    participations = Participation.objects.filter(user=user, status='registered')
    return render(request, 'events/my_account.html', {'organized_events': organized_events,
                                                      'participations': participations})

