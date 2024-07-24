from django.shortcuts import render
import requests
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Player, Game, Bet
from .serializers import TeamSerializer, PlayerSerializer, GameSerializer, BetSerializer

# Set up logging
logger = logging.getLogger(__name__)

class TeamAPIView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class PlayerAPIView(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

def fetch_games_from_api(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

class GameAPIView(APIView):
    def get(self, request):
        # API URLs for current and upcoming games
        current_games_url = 'curl -X GET http://api.football-data.org/v4/competitions/2003/matches?matchday=1 -H "X-Unfold-Goals: true"'
        upcoming_games_url = 'curl -X GET http://api.football-data.org/v4/competitions/2003/matches?matchday=1 -H "X-Unfold-Goals: true"'
        headers = {'X-Auth-Token': '34f8c3b470814eacab4e0200b0248aa8'}  # Replace with your actual API key

        current_games = fetch_games_from_api(current_games_url, headers)
        upcoming_games = fetch_games_from_api(upcoming_games_url, headers)

        if current_games is not None and upcoming_games is not None:
            response_data = {
                'current_games': current_games,
                'upcoming_games': upcoming_games
            }
            return Response(response_data)
        else:
            return Response({"error": "Unable to fetch games from external API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BetAPIView(APIView):
    def get(self, request):
        bets = Bet.objects.all()
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)
