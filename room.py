__author__ = 'DWA'

class Room(object):
    def __init__(self,id,x,y,w,h):
        self.id=id
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def printRoomStatsAsCLI(self):
        print("N"+str(self.id))
        print("X"+str(self.x))
        print("Y"+str(self.y))
        print("W"+str(self.w))
        print("H"+str(self.h))
        print("")