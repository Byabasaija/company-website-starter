from django.urls import path
from . import views

urlpatterns = [
    path('',          views.home_view,     name='home'),
    path('about/',    views.about_view,    name='about'),
    path('team/',     views.team_redirect, name='team'),
    path('services/', views.services_view, name='services'),
]
