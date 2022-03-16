from django.shortcuts import render
from .models import Post
from django.views.generic import TemplateView
import main.ChessGame
import json
from django.http import HttpResponse
from Games.models import GameSession 
from django.http import JsonResponse
import numpy as np
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
"""
def home(request):
    games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
 
    context = {"games": games}
    return render(request, 'main/lobby_game.html',context)


def about(request):
    return render(request, 'main/about.html', {'title': 'About'})
"""
class PlayGame(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "about.html"
    def get(self, request, format=None, *args, **kwargs):
        data = {"ena":2}
        return Response(data)
"""

def game(request):
    
    if request.method =="GET":
       
        if request.GET.get("create",None):
            context = {}
            return render(request, 'main/create_game.html',context)

        elif request.GET.get("id"):
            gamesess = GameSession.objects.get(gameid=request.GET.get("id"))
            gameid = request.GET.get("id")

            context = {"gameid":gameid, "update":True }
            return render(request, 'main/board.html',context)
        else: #request.GET.get("join",None):

            games = GameSession.objects.filter(isPrivate=False).filter(isFinished=False)
            print(games)
            context = {"games": games}
            return render(request, 'main/lobby_game.html',context)
    elif request.method == "POST":
     
        if request.POST.get("create",None)=="true":
            gamesess = GameSession(player1 = request.user, player2= None, name = request.POST.get("name","My Game!"), isPrivate = request.POST.get("isPrivate",False)=="on" )
            gamesess.save()
        elif request.POST.get("join",None):
            gamesess = GameSession.objects.get(gameid=request.GET.get("id"))
            if gamesess:
                gamesess.player2 = request.user
                gamesess.save()

        context = {
        
        }
    
        return render(request, 'main/lobby_game.html', context)

def play(request): #cambiar get por post
    if request.is_ajax and request.method =="GET":
     
        gameid = request.GET.get("id")
        user = request.user

        gamesess = GameSession.objects.get(gameid=request.GET.get("id"))

        if gamesess:
            prevmovs = json.loads(gamesess.moves)
         
            pos1,pos2 = [int(x) for x in request.GET.get("pos1")],[int(x) for x in request.GET.get("pos2")]
            current_mov =  len(prevmovs)%2 #leer json
            flag = False

            if current_mov==0:


                if user == gamesess.player1:
                    flag = True
            else:
                if user == gamesess.player2:
                    flag = True
            if flag:

            
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs+[(pos1,pos2)])
                if board is True:
                    gamesess.isFinished = True
                    gamesess.save()

                

                gamesess.moves = json.dumps(prevmovs+[(pos1,pos2)])
                gamesess.save()
                print(board)
            else:
                p2 = main.ChessGame.Player(s=-1)
                p1 = main.ChessGame.Player()

                shogi = main.ChessGame.Chess(p1=p1,p2=p2)
                
                board = shogi.play_moves(prevmovs)

                if board is True:
                    gamesess.isFinished = True
                    gamesess.save()
                
                gamesess.moves = json.dumps(prevmovs)
                gamesess.save()
        context = {"board":board.tolist()}
        return JsonResponse(context)
    elif request.method == "GET":

        context = {
        
        }
    
        return render(request, 'main/home.html', context)