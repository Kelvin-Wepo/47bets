from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from games.models import Game, Team
from django.contrib import messages


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_superuser)
def match(request):
    # Retrieve current and upcoming games
    current_games = Game.objects.filter(datetime__lte=timezone.now(), datetime_end__gt=timezone.now())
    upcoming_games = Game.objects.filter(datetime__gt=timezone.now())

    context = {
        'current_games': current_games,
        'upcoming_games': upcoming_games
    }

    return render(request, 'bureau/match.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game
    }
    return render(request, 'bureau/detail.html', context)


def roster(request):
    home_team_name = request.GET.get('home_team')
    away_team_name = request.GET.get('away_team')

    home_team = Team.objects.filter(name=home_team_name).first()
    away_team = Team.objects.filter(name=away_team_name).first()

    context = {
        'home_team': home_team,
        'away_team': away_team
    }

    return render(request, 'bureau/roster.html', context)


def terminate_match(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # Perform the necessary actions to terminate the match
    # For example, update the end time of the game
    
    game.datetime_end = timezone.now()
    game.save()
    success_message = 'Game has been terminated.'
    messages.success(request, success_message)
    # Redirect back to the match URL
    return redirect('bureau:match')


