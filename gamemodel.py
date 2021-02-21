__author__ = 'DWA'

import random

from level import Level
from player import Player

class GameModel(object):

    def __init__(self):
        self.levels=Level()

        playerStartLocationValid=False
        while playerStartLocationValid==False:
            px=random.randint(self.levels.mapBorder+1,self.levels.width-self.levels.mapBorder)
            py=random.randint(self.levels.mapBorder+1,self.levels.height-self.levels.mapBorder)
            if self.levels.tiles[px][py]>0 and self.levels.tiles[px][py]<1000:
                self.player=Player(px,py,0,15)
                playerStartLocationValid=True