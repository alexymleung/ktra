from django.urls import path
from . import views

urlpatterns = [
    path('type/<str:service_type>',views.services,name='services'),
    path('<int:service_id>',views.service,name='service'),
]