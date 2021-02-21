__author__ = 'DWA'

import pickle

class Player(object):
    def __init__(self,x,y,f,h):
        self.x=x
        self.y=y
        self.f=f
        self.h=h

    def savePlayer(self,playerInstance):
        pickle.dump( playerInstance, open( "player.sav", "wb" ) )

    def loadPlayer(self):
        playerInstance = pickle.load( open( "player.sav", "rb" ) )
        return playerInstance

    def printPlayerStatsAsCLI(self):
        print("X"+str(self.x))
        print("Y"+str(self.y))
        print("F"+str(self.f))
        print("H"+str(self.h))
        print("")