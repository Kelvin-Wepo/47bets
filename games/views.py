from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Player, Game, Bet
from .serializers import TeamSerializer, PlayerSerializer, GameSerializer, BetSerializer
import requests  

# Replace with your actual RapidAPI key and sports API endpoint URL
RAPIDAPI_KEY = "901a016350mshf8b45c31629586cp131677jsnea249d76ad10"
SPORTS_API_URL = "rapidapi.com"

# This view fetches sports data from the API and returns it
class GetSportsDataView(APIView):
    """Fetches sports data from the specified API."""

    def get(self, request):
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "rapidapi.com"  # Replace with actual host
        }

        try:
            response = requests.get(SPORTS_API_URL, headers=headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            data = response.json()
            return Response(data, status=200)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching sports data: {e}")
            return Response({"error": "An error occurred while fetching data"}, status=500)
        
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

class GameAPIView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

class BetAPIView(APIView):
    def get(self, request):
        bets = Bet.objects.all()
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)
 