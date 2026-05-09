from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='newsletter-subscribe'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='newsletter-unsubscribe'),
]
