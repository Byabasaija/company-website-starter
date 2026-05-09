from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile-list'),
    path('<slug:slug>/', views.profile_detail, name='profile-detail'),
]
