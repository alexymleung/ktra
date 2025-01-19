# events/urls.py 
from django.urls import path
from . import views

urlpatterns = [
    path('type/<str:event_type>/', views.events, name='events'),
    path('<int:event_id>/', views.event, name='event_detail'),
    path('search', views.search, name='e-search'),
]
