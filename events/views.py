from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def event_list(request):
    events = Event.objects.filter(is_finished=False).order_by('date')

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
    category_ids = request.GET.getlist('categories')
    if category_ids:
        events = events.filter(categories__id__in=category_ids).distinct()
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        events = events.filter(categories__id__in=selected_categories).distinct()

    return render(request, 'events/event_list.html', {'events': events, 'categories': categories,
                                                      'selected_categories': selected_categories})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participation_set.filter(status='registered')
    comments = event.comments.all().order_by('created_at')
    comment_form = CommentForm() if request.user.is_authenticated else None
    return render(request, 'events/event_detail.html', {'event': event, 'participants': participants,
                                                        'comments': comments, 'comment_form': comment_form})

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
    active_events = organized_events.filter(is_finished=False)
    finished_events = organized_events.filter(is_finished=True)
    participations = Participation.objects.filter(user=user, status='registered')
    return render(request, 'events/my_account.html', {'organized_events': organized_events,
                                                      'participations': participations,
                                                      'active_events': active_events,
                                                      'finished_events': finished_events})

@login_required
def add_comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.event = event
            comment.save()
            return redirect('event_detail', event_id=event_id)
    else:
        form = CommentForm()

    return render(request, 'events/add_comment.html', {'form': form, 'event': event})


@login_required
def add_review(request, event_id):

    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = ReviewForm()

    return render(request, 'events/add_review.html', {'form': form, 'event': event})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Только организатор может редактировать мероприятие
    if request.user != event.organizer:
        return HttpResponse("Доступ запрещен", status=403)

    # Если мероприятие завершено, редактирование запрещено
    if event.is_finished:
        return HttpResponse("Невозможно редактировать завершенное мероприятие.", status=403)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


@login_required
def finish_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        return HttpResponse("Доступ запрещен", status=403)

    if not event.is_finished:
        event.is_finished = True
        event.save()

    return redirect('event_detail', event_id=event.id)


def organizer_profile(request, organizer_id):
    organizer = get_object_or_404(User, pk=organizer_id)

    active_events = Event.objects.filter(organizer=organizer, is_finished=False).order_by('date')
    finished_events = Event.objects.filter(organizer=organizer, is_finished=True).order_by('date')
    return render(request, 'events/organizer_profile.html', {'organizer': organizer,
                                                             'active_events': active_events,
                                                             'finished_events': finished_events})