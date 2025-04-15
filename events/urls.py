from django.urls import path
from . import views




urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/finish/', views.finish_event, name='finish_event'),
    path('event/<int:event_id>/participate', views.participate_event, name='participate_event'),
    path('registration/', views.registration, name='registration'),
    path('my_account/', views.my_account, name='my_account'),
    path('event/<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
    path('event/<int:event_id>/add_review/', views.add_review, name='add_review'),
    path('organizer/<int:organizer_id>/', views.organizer_profile, name='organizer_profile'),
    path('event/<int:event_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),

]

