from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
import random


class Team(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Clean the team name by removing leading/trailing whitespaces
        self.name = self.name.strip()
        
        # Call the superclass's save() method to save the object
        super().save(*args, **kwargs)


class Player(models.Model):
    first_name = models.CharField(max_length=100, blank=False, default=None)
    last_name = models.CharField(max_length=100, blank=False, default=None)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=None, null=True)
    player_number = models.PositiveIntegerField(default=None, null=True)
    state = models.CharField(max_length=100, default=None, null=True)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    score = models.CharField(max_length=10, blank=True, null=True)
    commentary = models.TextField(blank=True, null=True)
    weather = models.CharField(max_length=100, blank=True, null=True)
    home_team_odds = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    away_team_odds = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    duration = models.DurationField(default=timedelta(hours=1))
    datetime = models.DateTimeField(default=None, null=True)
    datetime_end = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # New game being created
            self.datetime_end = self.datetime + self.duration

        if self.datetime_end <= timezone.now() and not self.score:
            # Game is over and score hasn't been generated yet, generate random score
            self.generate_random_score()

        super().save(*args, **kwargs)

        # Update bet results
        bets = Bet.objects.filter(game=self)
        for bet in bets:
            bet_result = bet.determine_result()
            bet.result = bet_result
            bet.save()

    def generate_random_score(self):
        home_score = random.randint(0, 30)
        away_score = random.randint(0, 30)
        self.score = f"{home_score} - {away_score}"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.datetime}"
   
     
class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, default=None)
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2)
    result = models.BooleanField(null=True, blank=True)
    
    def determine_result(self):
        if self.game.score:
            home_score, away_score = map(int, self.game.score.split('-'))
            if self.team == self.game.home_team and home_score > away_score:
                return True  # Bet won
            elif self.team == self.game.away_team and away_score > home_score:
                return True  # Bet won
            else:
                return False  # Bet lost
        else:
            return None  # Result pending
    
    def __str__(self):
        return f"{self.user.username} - {self.game}"

    def save(self, *args, **kwargs):
        self.result = self.determine_result()
        super().save(*args, **kwargs)