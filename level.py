__author__ = 'DWA'

import random,pickle
from room import Room
from hall import Hall
from connector import Connector
from configparser import ConfigParser

config=ConfigParser()
config.read('config.ini')

VERBOSE_ROOMS=config.getboolean('DEBUG','VERBOSE_ROOMS')
VERBOSE_HALLS=config.getboolean('DEBUG','VERBOSE_HALLS')
VERBOSE_CONNECTORS=config.getboolean('DEBUG','VERBOSE_CONNECTORS')

class Level(object):
    def __init__(self):
        self.width = 2*(config.getint('LEVEL PARAMS','gWidth')//2)+1                    # ODD ONLY
        self.height = 2*(config.getint('LEVEL PARAMS','gHeight')//2)+1                  # ODD ONLY
        self.maxRoomsPerLevel = config.getint('LEVEL PARAMS','maxRoomsPerLevel')
        self.maxRoomAttempts = config.getint('LEVEL PARAMS','maxRoomPlacementAttempts')
        self.maxRoomWidth = 2*(config.getint('LEVEL PARAMS','maxRmWidth')//2)+1         # ODD ONLY
        self.minRoomWidth = 2*(config.getint('LEVEL PARAMS','minRmWidth')//2)+1         # ODD ONLY
        self.maxRoomHeight = 2*(config.getint('LEVEL PARAMS','maxRmHeight')//2)+1       # ODD ONLY
        self.minRoomHeight = 2*(config.getint('LEVEL PARAMS','minRmHeight')//2)+1       # ODD ONLY
        self.minRoomGap = 2*(config.getint('LEVEL PARAMS','minRoomGap')//2)+1           # ODD ONLY
        self.mapBorder = 2*(config.getint('LEVEL PARAMS','mapBorder')//2)+1             # ODD ONLY
        self.createSecretDoors = config.getboolean('LEVEL PARAMS','createSecretDoors')
        self.miniMapGM = config.getboolean('GOD MODE','miniMapGM')

        self.tiles = [ [ 0 for x in range(self.height) ] for y in range(self.width) ]
        self.visitedTiles = [ [ self.miniMapGM for x in range(self.height) ] for y in range(self.width) ]
        self.rooms = []
        self.addRooms()
        self.halls = []
        self.ci = 0
        self.cj = 0
        self.addHalls()
        self.connectors = []
        self.addConnectors()
        self.promoteConnectorsToDoors()
        if self.createSecretDoors == True:
            self.promoteConnectorsToSecretDoors()
        self.removeUnusedConnectors()
        self.removeDeadEnds()
        self.createFalseRooms()
        self.createHallSeparators()
        self.printLevelStatsAsCLI()

    def get_maxRooms(self):
        return self.maxRoomAttempts

    def addRooms(self):
        for r in range(self.maxRoomAttempts):
            if (len(self.rooms)==self.maxRoomsPerLevel):
                break
            randomW=2*(random.randint(self.minRoomWidth,self.maxRoomWidth)//2)+1                    # ODD ONLY
            randomH=2*(random.randint(self.minRoomWidth,self.maxRoomHeight)//2)+1                   # ODD will not change
            randomX=2*(random.randint(self.mapBorder,self.width-randomW-self.mapBorder)//2)+1       # but EVEN will increase by 1
            randomY=2*(random.randint(self.mapBorder,self.height-randomH-self.mapBorder)//2)+1
            if self.validateNewRoom(randomX,randomY,randomW,randomH) == True:
                self.rooms.append(Room(len(self.rooms)+1,randomX,randomY,randomW,randomH))
                for i in range(randomX,randomX+randomW):
                    for j in range(randomY,randomY+randomH):
                        self.tiles[i][j]=len(self.rooms)

    def validateNewRoom(self,x,y,w,h):
        newRoomIsValid=True
        for i in range(x-self.minRoomGap,x+w+self.minRoomGap):
            for j in range (y-self.minRoomGap,y+h+self.minRoomGap):
                if i<0: i=0
                if i>=self.width: i=self.width-1
                if j<0: j=0
                if j>=self.height: j=self.height-1
                if self.tiles[i][j] != 0:
                    newRoomIsValid=False
        return newRoomIsValid

    def addHalls(self):
        while self.seedHall()==True:
            self.carveHall()
            cid=len(self.halls)
            while len(self.halls[cid-1].crumbs)>0:
                self.reverseCarveHall()

    def seedHall(self):
        foundSeed=False
        for i in range(self.mapBorder,self.width-self.mapBorder,2):
            for j in range(self.mapBorder,self.height-self.mapBorder,2):
                if self.tiles[i][j]==0 and foundSeed==False:
                    cid=len(self.halls)+1
                    self.halls.append(Hall(cid))
                    self.tiles[i][j]=-cid
                    self.ci=i
                    self.cj=j
                    foundSeed=True
        return foundSeed

    def carveHall(self):
        keepCarving=True
        while keepCarving:
            i=self.ci
            j=self.cj
            validDirs=[]
            n=j-2
            s=j+2
            w=i-2
            e=i+2
            if (n>=self.mapBorder and n<self.width-self.mapBorder and self.tiles[i][n]==0):
                validDirs.append("n")
            if (s>=self.mapBorder and s<self.width-self.mapBorder and self.tiles[i][s]==0):
                validDirs.append("s")
            if (w>=self.mapBorder and w<self.width-self.mapBorder and self.tiles[w][j]==0):
                validDirs.append("w")
            if (e>=self.mapBorder and e<self.width-self.mapBorder and self.tiles[e][j]==0):
                validDirs.append("e")
            if len(validDirs)==0:
                keepCarving=False
                cid=len(self.halls)
                self.halls[cid-1].crumbs.append((self.ci,self.cj))
                self.halls[cid-1].paths.append((self.ci,self.cj))
            else:
                dir=random.choice(validDirs)
                cid=len(self.halls)
                self.halls[cid-1].crumbs.append((self.ci,self.cj))
                self.halls[cid-1].paths.append((self.ci,self.cj))
                cid=len(self.halls)
                if dir=="n":
                    self.tiles[i][j-1]=-cid
                    self.tiles[i][j-2]=-cid
                    self.ci=i
                    self.cj=j-2
                if dir=="s":
                    self.tiles[i][j+1]=-cid
                    self.tiles[i][j+2]=-cid
                    self.ci=i
                    self.cj=j+2
                if dir=="w":
                    self.tiles[i-1][j]=-cid
                    self.tiles[i-2][j]=-cid
                    self.ci=i-2
                    self.cj=j
                if dir=="e":
                    self.tiles[i+1][j]=-cid
                    self.tiles[i+2][j]=-cid
                    self.ci=i+2
                    self.cj=j
        cid=len(self.halls)
        self.halls[cid-1].crumbs.pop()
        lc=len(self.halls[cid-1].crumbs)
        if lc>0:
            self.ci=self.halls[cid-1].crumbs[lc-1][0]
            self.cj=self.halls[cid-1].crumbs[lc-1][1]

    def reverseCarveHall(self):
        keepCarving=True
        while keepCarving==True:
            i=self.ci
            j=self.cj
            validDirs=[]
            n=j-2
            s=j+2
            w=i-2
            e=i+2
            if (n>=self.mapBorder and n<self.height-self.mapBorder and self.tiles[i][n]==0):
                validDirs.append("n")
            if (s>=self.mapBorder and s<self.height-self.mapBorder and self.tiles[i][s]==0):
                validDirs.append("s")
            if (w>=self.mapBorder and w<self.width-self.mapBorder and self.tiles[w][j]==0):
                validDirs.append("w")
            if (e>=self.mapBorder and e<self.width-self.mapBorder and self.tiles[e][j]==0):
                validDirs.append("e")
            if len(validDirs)==0:
                keepCarving=False
            else:
                dir=random.choice(validDirs)
                cid=len(self.halls)
                self.halls[cid-1].crumbs.append((self.ci,self.cj))

                cid=len(self.halls)
                if dir=="n":
                    self.tiles[i][j-1]=-cid
                    self.tiles[i][j-2]=-cid
                    self.ci=i
                    self.cj=j-2
                    self.halls[cid-1].paths.append((self.ci,self.cj))
                if dir=="s":
                    self.tiles[i][j+1]=-cid
                    self.tiles[i][j+2]=-cid
                    self.ci=i
                    self.cj=j+2
                    self.halls[cid-1].paths.append((self.ci,self.cj))
                if dir=="w":
                    self.tiles[i-1][j]=-cid
                    self.tiles[i-2][j]=-cid
                    self.ci=i-2
                    self.cj=j
                    self.halls[cid-1].paths.append((self.ci,self.cj))
                if dir=="e":
                    self.tiles[i+1][j]=-cid
                    self.tiles[i+2][j]=-cid
                    self.ci=i+2
                    self.cj=j
                    self.halls[cid-1].paths.append((self.ci,self.cj))
        cid=len(self.halls)
        self.halls[cid-1].crumbs.pop()
        lc=len(self.halls[cid-1].crumbs)
        if lc>0:
            self.ci=self.halls[cid-1].crumbs[lc-1][0]
            self.cj=self.halls[cid-1].crumbs[lc-1][1]

    def addConnectors(self):
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                for k in range(-1,2,2):
                    if self.tiles[i-1][j]!=self.tiles[i+1][j] and self.tiles[i][j]==0 and self.tiles[i-1][j]!=0 and self.tiles[i+1][j]!=0 and self.tiles[i-1][j]!=1000 and self.tiles[i+1][j]!=1000:
                        self.tiles[i][j]=1000
                        self.connectors.append(Connector(len(self.connectors)+1,i,j,self.tiles[i-1][j],self.tiles[i+1][j],0))
                    if self.tiles[i][j-1]!=self.tiles[i][j+1] and self.tiles[i][j]==0 and self.tiles[i][j-1]!=0 and self.tiles[i][j+1]!=0 and self.tiles[i][j-1]!=1000 and self.tiles[i][j+1]!=1000:
                        self.tiles[i][j]=1000
                        self.connectors.append(Connector(len(self.connectors)+1,i,j,self.tiles[i][j+1],self.tiles[i][j-1],0))

    def promoteConnectorsToDoors(self):
        unConnectedRegions=[]
        for ur in range(len(self.rooms)):
            unConnectedRegions.append(self.rooms[ur].id)
        for uh in range(len(self.halls)):
            unConnectedRegions.append(-self.rooms[uh].id)
        connectedRegions=[]
        regionSeed=random.choice(unConnectedRegions)
        connectedRegions.append(regionSeed)
        while len(unConnectedRegions) > 0:
            possibleConnectors=[]
            for c in range(len(self.connectors)):
                pc=self.connectors[c]
                if (pc.reg1 in connectedRegions and pc.reg2 not in connectedRegions) or (pc.reg2 in connectedRegions and pc.reg1 not in connectedRegions):
                    possibleConnectors.append(pc)
            cpc=random.choice(possibleConnectors)
            cpc.type=1
            self.tiles[cpc.x][cpc.y]=1001
            if cpc.reg1 in unConnectedRegions:
                unConnectedRegions.remove(cpc.reg1)
            if cpc.reg2 in unConnectedRegions:
                unConnectedRegions.remove(cpc.reg2)
            connectedRegions.append(cpc.reg1)
            connectedRegions.append(cpc.reg2)

    def promoteConnectorsToSecretDoors(self):
        maxCount=100
        for r in range(len(self.connectors)):
            randInt=random.randint(0,maxCount)
            if self.connectors[r].type==0 and randInt<maxCount//10 and self.tiles[self.connectors[r].x+1][self.connectors[r].y]<1001 and self.tiles[self.connectors[r].x-1][self.connectors[r].y]<1001 and self.tiles[self.connectors[r].x][self.connectors[r].y+1]<1001 and self.tiles[self.connectors[r].x][self.connectors[r].y-1]<1001:
                self.connectors[r].type=2
                self.tiles[self.connectors[r].x][self.connectors[r].y]=1002

    def removeUnusedConnectors(self):
        for c in range(len(self.connectors)):
            pc=self.connectors[c]
            if pc.type==-1 or pc.type==0:
                # type -1 are invalid connectors
                # type 0 connectors are initially valid but later discarded
                self.tiles[pc.x][pc.y]=0

    def removeDeadEnds(self):
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                numEmpty=0
                if self.tiles[i-1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j]!=1001 and self.tiles[i-1][j]!=1001 and self.tiles[i][j+1]!=1001 and self.tiles[i][j-1]!=1001 and self.tiles[i][j]<0 and numEmpty >6:
                    self.tiles[i][j]=0
        for i in range(self.width-self.mapBorder-1,self.mapBorder,-1):
            for j in range(self.height-self.mapBorder-1,self.mapBorder,-1):
                numEmpty=0
                if self.tiles[i-1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j]!=1001 and self.tiles[i-1][j]!=1001 and self.tiles[i][j+1]!=1001 and self.tiles[i][j-1]!=1001 and self.tiles[i][j]<0 and numEmpty >6:
                    self.tiles[i][j]=0

        for h in range(len(self.halls)):
            self.halls[h].paths=[]
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                if self.tiles[i][j]<0:
                    self.halls[self.tiles[i][j]].paths.append((i,j))
        for h in range(len(self.halls)):
            self.halls[h].paths.sort()

    def createFalseRooms(self):
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                numEmpty=0
                if self.tiles[i-1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j+1]==0: numEmpty=numEmpty+1
                if self.tiles[i][j-1]==0: numEmpty=numEmpty+1
                if self.tiles[i+1][j]==0: numEmpty=numEmpty+1
                if self.tiles[i-1][j]==0: numEmpty=numEmpty+1
                inRoom=False
                for di in range(-1,2):
                    for dj in range(-1,2):
                        if self.tiles[i+di][j+dj]>0:
                            inRoom=True
                if self.tiles[i][j]==0 and numEmpty==7 and inRoom==False and self.tiles[i+1][j+1]==0 and self.tiles[i-1][j-1]==0 and self.tiles[i+1][j-1]==0 and self.tiles[i-1][j+1]==0:
                    self.tiles[i][j]=9998

    def createHallSeparators(self):
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                noDefects=True
                if j+2<self.height-self.mapBorder:
                    if self.tiles[i+1][j+2]!=0: noDefects=False
                if self.tiles[i+1][j+1]!=0: noDefects=False
                if self.tiles[i+1][j]!=0: noDefects=False
                if self.tiles[i+1][j-1]!=0: noDefects=False
                if j-2>self.mapBorder:
                    if self.tiles[i+1][j-2]!=0: noDefects=False
                if j+2<self.height-self.mapBorder:
                    if self.tiles[i-1][j+2]!=0: noDefects=False
                if self.tiles[i-1][j+1]!=0: noDefects=False
                if self.tiles[i-1][j]!=0: noDefects=False
                if self.tiles[i-1][j-1]!=0: noDefects=False
                if j-2>self.mapBorder:
                    if self.tiles[i-1][j-2]!=0: noDefects=False
                maxCount=100
                randInt=random.randint(0,maxCount)
                if randInt<maxCount//4 and self.tiles[i][j]<0 and self.tiles[i][j+1]<0 and self.tiles[i][j-1]<0 and self.tiles[i][j+2]<0 and self.tiles[i][j-2]<0 and noDefects==True:
                    self.tiles[i][j]=9999
        for i in range(self.mapBorder,self.width-self.mapBorder):
            for j in range(self.mapBorder,self.height-self.mapBorder):
                noDefects=True
                if i+2<self.width-self.mapBorder:
                    if self.tiles[i+2][j+1]!=0: noDefects=False
                if self.tiles[i+1][j+1]!=0: noDefects=False
                if self.tiles[i][j+1]!=0: noDefects=False
                if self.tiles[i+1][j+1]!=0: noDefects=False
                if i-2>self.mapBorder:
                    if self.tiles[i-2][j+1]!=0: noDefects=False
                if i-2>self.mapBorder:
                    if self.tiles[i-2][j-1]!=0: noDefects=False
                if self.tiles[i-1][j-1]!=0: noDefects=False
                if self.tiles[i][j-1]!=0: noDefects=False
                if self.tiles[i+1][j-1]!=0: noDefects=False
                if i+2<self.width-self.mapBorder:
                    if self.tiles[i+2][j-1]!=0: noDefects=False
                maxCount=100
                randInt=random.randint(0,maxCount)
                if randInt<maxCount//4 and self.tiles[i][j]<0 and self.tiles[i+1][j]<0 and self.tiles[i-1][j]<0 and self.tiles[i+2][j]<0 and self.tiles[i-2][j]<0 and noDefects==True:
                    self.tiles[i][j]=9999

    def printLevelStatsAsCLI(self):
        r=len(self.rooms)
        if VERBOSE_ROOMS == True:
            print("Verbose Room Info")
            print("")
            for i in range(r):
                self.rooms[i].printRoomStatsAsCLI()
        print("# Rooms: "+str(r))
        print("")
        h=len(self.halls)
        if VERBOSE_HALLS == True:
            print("Verbose Hall Info")
            print("")
            for i in range(h):
                self.halls[i].printHallStatsAsCLI()
        print("# Halls: "+str(h))
        print("")

        c=len(self.connectors)
        ci=0 #count of invalid connectors
        cd=0 #count of door connectors
        cs=0 #count of secret connectors
        cf=0 #count of failed connectors (valid but unused)
        if VERBOSE_CONNECTORS == True:
            print("Verbose Connector Info")
            print("")
            for i in range(c):
                if VERBOSE_CONNECTORS == True:
                    self.connectors[i].printConnStatsAsCLI()
                if self.connectors[i].type==-1:
                    ci=ci+1
                if self.connectors[i].type==0:
                    cf=cf+1
                if self.connectors[i].type==1:
                    cd=cd+1
                if self.connectors[i].type==2:
                    cs=cs+1
            print("# Connectors (invalid): "+str(ci))
            print("# Connectors (normal): "+str(cd))
            print("# Connectors (secret): "+str(cs))
            print("# Connectors (failed): "+str(cf))
        print("# Connectors: "+str(c))
        print("")

    def saveLevel(self,levelInstance):
        pickle.dump( levelInstance, open( "level.sav", "wb" ) )

    def loadLevel(self):
        levelInstance = pickle.load( open( "level.sav", "rb" ) )
        return levelInstance