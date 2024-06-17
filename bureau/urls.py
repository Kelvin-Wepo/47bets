from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'bureau'

urlpatterns = [
    path('match/', login_required(views.match), name='match'),
    path('detail/<int:game_id>/', views.detail, name='detail'),
    path('match/<int:game_id>/terminate/', views.terminate_match, name='terminate_match'),
]