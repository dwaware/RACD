__author__ = 'DWA'

import pygame
from pygame.locals import *

from gamemodel import GameModel
from gameview import GameView

class Game(object):

    def __init__(self):
        self.running = True
        self.gameModel = GameModel()
        self.view = GameView()
        self.runGame()

    def newGame(self):
        game.__init__()

    def saveGame(self):
        game.gameModel.player.savePlayer(game.gameModel.player)
        game.gameModel.levels.saveLevel(game.gameModel.levels)

    def loadGame(self):
         game.gameModel.player = game.gameModel.player.loadPlayer()
         game.gameModel.levels = game.gameModel.levels.loadLevel()

    def pauseGame(self):
        if self.running==True:
            self.running=False
        else:
            self.running=True

    def runGame(self):
        while self.running==True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_w: #N
                        if self.gameModel.player.y>self.gameModel.levels.mapBorder and self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y-1]!=0:
                            self.gameModel.player.y=self.gameModel.player.y-1
                            self.gameModel.player.f=0
                    elif event.key==pygame.K_a: #W
                        if self.gameModel.player.x>self.gameModel.levels.mapBorder and self.gameModel.levels.tiles[self.gameModel.player.x-1][self.gameModel.player.y]!=0:
                            self.gameModel.player.x=self.gameModel.player.x-1
                            self.gameModel.player.f=3
                    elif event.key==pygame.K_s: #S
                        if self.gameModel.player.y<self.gameModel.levels.height-self.gameModel.levels.mapBorder-1 and self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y+1]!=0:
                            self.gameModel.player.y=self.gameModel.player.y+1
                            self.gameModel.player.f=2
                    elif event.key==pygame.K_d: #E
                        if self.gameModel.player.x<self.gameModel.levels.width-self.gameModel.levels.mapBorder-1 and self.gameModel.levels.tiles[self.gameModel.player.x+1][self.gameModel.player.y]!=0:
                            self.gameModel.player.x=self.gameModel.player.x+1
                            self.gameModel.player.f=1
                    elif event.key==pygame.K_UP:
                        self.gameModel.player.f=0
                    elif event.key==pygame.K_RIGHT:
                        self.gameModel.player.f=1
                    elif event.key==pygame.K_DOWN:
                        self.gameModel.player.f=2
                    elif event.key==pygame.K_LEFT:
                        self.gameModel.player.f=3
                    #print("X"+str(self.gameModel.player.x)+ " Y"+str(self.gameModel.player.y))
                    #hID=self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y]
                    #if hID<0:
                    #    print(hID)
                    #    self.gameModel.levels.halls[hID].printHallStatsAsCLI()
                    if self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y] == 1002:
                        print("Using a secret door!")
                    for si in range(-1,2):
                        for sj in range(-1,2):
                            if self.gameModel.levels.tiles[self.gameModel.player.x+si][self.gameModel.player.y+sj] == 9998:
                                if si==0 and sj==0:
                                    print("A trap!")
                                else:
                                    print("A trap nearby!")
                    if self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y] == 9999:
                        print("The corridor continues!")
                        if self.gameModel.levels.tiles[self.gameModel.player.x-1][self.gameModel.player.y]==self.gameModel.levels.tiles[self.gameModel.player.x+1][self.gameModel.player.y] and self.gameModel.levels.tiles[self.gameModel.player.x-1][self.gameModel.player.y]!=0:
                            self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y]=self.gameModel.levels.tiles[self.gameModel.player.x-1][self.gameModel.player.y]
                            #print(self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y])
                        elif self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y-1]==self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y+1] and self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y-1]!=0:
                            self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y]=self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y-1]
                            #print(self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y])
                if event.type == QUIT:
                    pygame.quit()
                    self.running=False
            for rx in range(self.gameModel.player.x-1,self.gameModel.player.x+2):
                for ry in range(self.gameModel.player.y-1,self.gameModel.player.y+2):
                    if (self.gameModel.levels.tiles[rx][ry]!=1002):
                        self.gameModel.levels.visitedTiles[rx][ry]=1
                    else:
                        if self.gameModel.player.x==rx and self.gameModel.player.y==ry:
                            self.gameModel.levels.visitedTiles[rx][ry]=1
            rID=self.gameModel.levels.tiles[self.gameModel.player.x][self.gameModel.player.y]-1
            if rID>=0 and rID<1000:
                rmx=self.gameModel.levels.rooms[rID].x
                rmy=self.gameModel.levels.rooms[rID].y
                rmw=self.gameModel.levels.rooms[rID].w
                rmh=self.gameModel.levels.rooms[rID].h
                for rmxx in range(rmx-1,rmx+rmw+1):
                    for rmyy in range(rmy-1,rmy+rmh+1):
                        if self.gameModel.levels.tiles[rmxx][rmyy]!=1002:
                            self.gameModel.levels.visitedTiles[rmxx][rmyy]=1
            if self.running==True:
                self.view.refreshMiniMap(self.gameModel)
                self.view.refreshTacMap(self.gameModel)

game = Game()