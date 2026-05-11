from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile-list'),
    path('<slug:category_slug>/', views.profile_category, name='profile-category'),
    path('<slug:category_slug>/<slug:profile_slug>/', views.profile_detail, name='profile-detail'),
]
