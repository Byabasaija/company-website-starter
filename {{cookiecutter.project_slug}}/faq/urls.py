from django.urls import path
from . import views

urlpatterns = [
    path('', views.faq_index, name='faq'),
]
