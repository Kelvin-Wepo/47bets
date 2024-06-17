from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('roster/', views.roster, name='roster'),
    path('bets/', views.bets, name='bets'),
] 