from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
import uuid

class GameSession(models.Model):
    #players = models.ManyToManyField(Profile)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1', null = True, blank=True)
    player2 = models.ForeignKey(User,  on_delete=models.SET_NULL, related_name='player2', null = True, blank=True)
    winner_player = models.ForeignKey(User,  on_delete=models.SET_NULL, related_name='winner_player', null = True, blank=True)
    moves = models.TextField(default = "[]",null=True)
    name = models.TextField(default="My Game!")
    gameid = models.UUIDField(default = uuid.uuid4)
    isFinished = models.BooleanField(default=False)
    isPrivate = models.BooleanField(default=False)