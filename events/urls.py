from django.urls import path
from . import views




urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/participate', views.participate_event, name='participate_event'),
    path('registration/', views.registration, name='registration'),
    path('my_account/', views.my_account, name='my_account')
]

