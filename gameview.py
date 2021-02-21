__author__ = 'DWA'

import pygame,math
import tileManager

from UIconstants import *

class GameView(object):

    def __init__(self):

        self.screen = pygame.display.set_mode((frameWidth-2*margin,frameHeight-2*margin))
        pygame.key.set_repeat(delay, interval)
        self.screen.fill(WHITE)
        pygame.display.init()
        pygame.display.flip()

        fn="res/tiles.png"
        self.tileArray = tileManager.loadTileTable(fn, 32, 32)
        self.imgRoomFloor = pygame.transform.scale(self.tileArray[56][16],(tSize-1,tSize-1))
        self.imgWall = pygame.transform.scale(self.tileArray[29][13],(tSize-1,tSize-1))
        self.imgHallFloor = pygame.transform.scale(self.tileArray[37][13],(tSize-1,tSize-1))
        self.imgHallTrap = pygame.transform.scale(self.tileArray[33][11],(tSize-1,tSize-1))
        self.imgHero = pygame.transform.scale(self.tileArray[43][1],(tSize//2-1,tSize//2-1))

    def refreshMiniMap(self,gameModel):
        miniMap = pygame.Surface((mmWidth,mmHeight))
        gWidth=gameModel.levels.width
        gHeight=gameModel.levels.height
        eSize=mmWidth//gWidth
        miniMap.fill(BLUE)

        ci=gameModel.player.x
        cj=gameModel.player.y
        adjIm=-(mmWidth-eSize*gWidth)//2
        adjJm=-(mmHeight-eSize*gHeight)//2

        for i in range(0,gameModel.levels.width):
            for j in range(0,gameModel.levels.height):
                if gameModel.levels.visitedTiles[i][j]==1:
                    if gameModel.levels.tiles[i][j]<0:
                        pygame.draw.rect(miniMap,(BROWN),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==0:
                        pygame.draw.rect(miniMap,(BLACK),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==1000:
                        pygame.draw.rect(miniMap,(BLUE),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==1001:
                        pygame.draw.rect(miniMap,(DARKBROWN),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==1002:
                        pygame.draw.rect(miniMap,(GREEN),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==9998:
                        pygame.draw.rect(miniMap,(RED),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    elif gameModel.levels.tiles[i][j]==9999:
                        #pygame.draw.rect(miniMap,(ORANGE),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1)) #DRAW IN ORANGE TO DEBUG
                        pygame.draw.rect(miniMap,(BROWN),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                    else:
                        pygame.draw.rect(miniMap,(GRAY),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                else:
                    pygame.draw.rect(miniMap,(BLACK),(i*eSize-adjIm,j*eSize-adjJm,eSize-1,eSize-1))
                if i==ci and j==cj:
                    pygame.draw.circle(miniMap,(WHITE),(i*eSize+eSize//2-adjIm,j*eSize+eSize//2-adjJm),eSize//2)
        self.screen.blit(miniMap, (tmWidth+100,margin))
        pygame.display.update()

    def refreshTacMap(self,gameModel):
        tacticalMap = pygame.Surface((tmHeight,tmWidth))
        gWidth=gameModel.levels.width
        gHeight=gameModel.levels.height
        tacticalMap.fill(BLUE)

        ci=gameModel.player.x
        cj=gameModel.player.y
        adjI=int((ci-tacMapWH/2)*tSize)
        adjJ=int((cj-tacMapWH/2)*tSize)

        rID=gameModel.levels.tiles[gameModel.player.x][gameModel.player.y]-1
        playerInRoom=False
        if rID>=0 and rID<1000:
            trmx=gameModel.levels.rooms[rID].x
            trmy=gameModel.levels.rooms[rID].y
            trmw=gameModel.levels.rooms[rID].w
            trmh=gameModel.levels.rooms[rID].h
            playerInRoom=True

        iPlusObstacle = maxTacMapRadius
        iMinusObstacle = maxTacMapRadius
        jMinusObstacle = maxTacMapRadius
        jPlusObstacle = maxTacMapRadius

        if playerInRoom==False:
            for opi in range(maxTacMapRadius,0,-1):
                if ci+opi>gWidth-1:
                    iPlusObstacle = opi
                else:
                    if gameModel.levels.tiles[ci+opi][cj]==0 or gameModel.levels.tiles[ci+opi][cj]==1001 or gameModel.levels.tiles[ci+opi][cj]==1002 or (gameModel.levels.tiles[ci+opi][cj]==9999 and gameModel.levels.visitedTiles[ci+opi][cj]==0):
                        iPlusObstacle = opi
            for omi in range(maxTacMapRadius,0,-1):
                if ci-omi<0:
                    iMinusObstacle = omi
                else:
                    if gameModel.levels.tiles[ci-omi][cj]==0 or gameModel.levels.tiles[ci-omi][cj]==1001 or gameModel.levels.tiles[ci-omi][cj]==1002 or (gameModel.levels.tiles[ci-omi][cj]==9999 and gameModel.levels.visitedTiles[ci-omi][cj]==0):
                        iMinusObstacle = omi

            for opj in range(maxTacMapRadius,0,-1):
                if cj+opj>gHeight-1:
                    jPlusObstacle = opj
                else:
                    if gameModel.levels.tiles[ci][cj+opj]==0 or gameModel.levels.tiles[ci][cj+opj]==1001 or gameModel.levels.tiles[ci][cj+opj]==1002 or (gameModel.levels.tiles[ci][cj+opj]==9999 and gameModel.levels.visitedTiles[ci][cj+opj]==0):
                        jPlusObstacle = opj
            for omj in range(maxTacMapRadius,0,-1):
                if cj-omj<0:
                    jMinusObstacle = omj
                else:
                    if gameModel.levels.tiles[ci][cj-omj]==0 or gameModel.levels.tiles[ci][cj-omj]==1001 or gameModel.levels.tiles[ci][cj-omj]==1002 or (gameModel.levels.tiles[ci][cj-omj]==9999 and gameModel.levels.visitedTiles[ci][cj-omj]==0):
                        jMinusObstacle = omj

        # visionDistanceLimit=maxTacMapRadius
        # reduce this below baseTacLimit to create reduced vision due to low lighting, etc.
        # ... and dist<maxTacMapRadius ...

        for i in range(ci-tacMapWH//2,ci+tacMapWH//2+1):
            for j in range(cj-tacMapWH//2,cj+tacMapWH//2+1):
                dist=math.sqrt((ci - i)**2 + (cj - j)**2)
                if i>-1 and i<gWidth and j>-1 and j<gHeight and (
                    playerInRoom==False and (
                        (((ci-i>=0 and ci-i<=iMinusObstacle) or (i-ci>=0 and i-ci<=iPlusObstacle)) and math.fabs(cj-j)<2)
                        or
                        (((cj-j>=0 and cj-j<=jMinusObstacle) or (j-cj>=0 and j-cj<=jPlusObstacle)) and math.fabs(ci-i)<2 ))
                    )or (
                    playerInRoom==True and i>trmx-2 and i<trmx+trmw+1 and j>trmy-2 and j<trmy+trmh+1):

                    if gameModel.levels.tiles[i][j]<0:
                        #pygame.draw.rect(tacticalMap,(BROWN),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                        tacticalMap.blit(self.imgHallFloor,[i*tSize-adjI,j*tSize-adjJ])
                    elif gameModel.levels.tiles[i][j]==0:
                        #pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                        tacticalMap.blit(self.imgWall,[i*tSize-adjI,j*tSize-adjJ])
                    elif gameModel.levels.tiles[i][j]==1000:
                        tacticalMap.blit(self.imgWall,[i*tSize-adjI,j*tSize-adjJ])
                        # unused connectors are drawn in blue but should NEVER APPEAR (NORMALLY TILES ARE SET TO "0")
                        pygame.draw.rect(tacticalMap,(BLUE),(i*tSize-adjI+tSize//4,j*tSize-adjJ+tSize//4,(tSize-1)//2,(tSize-1)//2))
                    elif gameModel.levels.tiles[i][j]==1001:
                        pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                        if dist!=0:
                            if gameModel.levels.tiles[i][j-1]==0 or gameModel.levels.tiles[i][j+1]==0 or gameModel.levels.tiles[i][j-1]==1000 or gameModel.levels.tiles[i][j+1]==1000:
                                pygame.draw.rect(tacticalMap,(DARKBROWN),(i*tSize-adjI+tSize//3,j*tSize-adjJ,tSize//3-1,tSize-1))
                            else:
                                pygame.draw.rect(tacticalMap,(DARKBROWN),(i*tSize-adjI,j*tSize-adjJ+tSize//3,tSize-1,tSize//3-1))
                    elif gameModel.levels.tiles[i][j]==1002:
                        #pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1)) # GREEN ON MINIMAP ONCE DISCOVERED
                        tacticalMap.blit(self.imgWall,[i*tSize-adjI,j*tSize-adjJ])
                        pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI+tSize//2,j*tSize-adjJ+tSize//2,2,2)) # THIS LINE SHOWS A HINT
                    elif gameModel.levels.tiles[i][j]==9998:
                        if gameModel.levels.visitedTiles[i][j]==1:
                            #pygame.draw.rect(tacticalMap,(RED),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                            tacticalMap.blit(self.imgHallFloor,[i*tSize-adjI,j*tSize-adjJ])
                            tacticalMap.blit(self.imgHallTrap,[i*tSize-adjI,j*tSize-adjJ])
                        else:
                            #pygame.draw.rect(tacticalMap,(BROWN),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                            tacticalMap.blit(self.imgHallFloor,[i*tSize-adjI,j*tSize-adjJ])
                    elif gameModel.levels.tiles[i][j]==9999:
                        if gameModel.levels.visitedTiles[i][j]==1:
                            tacticalMap.blit(self.imgHallFloor,[i*tSize-adjI,j*tSize-adjJ])
                            #pygame.draw.rect(tacticalMap,(ORANGE),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                        else:
                            #pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                            tacticalMap.blit(self.imgWall,[i*tSize-adjI,j*tSize-adjJ])
                            #pygame.draw.rect(tacticalMap,(DARKGRAY),(i*tSize-adjI+tSize//2,j*tSize-adjJ+tSize//2,2,2)) # THIS LINE SHOWS A HINT
                    else:
                        #pygame.draw.rect(tacticalMap,(GRAY),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))
                        tacticalMap.blit(self.imgRoomFloor,[i*tSize-adjI,j*tSize-adjJ])
                    if i==ci and j==cj:
                        #pygame.draw.circle(tacticalMap,(BLUE),(i*tSize-adjI+tSize//2,j*tSize-adjJ+tSize//2),tSize//3)
                        if gameModel.player.f==0: #N
                            fx=0
                            fy=-1
                            tacticalMap.blit(self.imgHero,[i*tSize+tSize//4-adjI,j*tSize+tSize//4-adjJ])
                        if gameModel.player.f==1: #E
                            fx=1
                            fy=0
                            rotHero = pygame.transform.rotate(self.imgHero,270)
                            tacticalMap.blit(self.imgHero,[i*tSize+tSize//4-adjI,j*tSize+tSize//4-adjJ])
                        if gameModel.player.f==2: #S
                            fx=0
                            fy=1
                            rotHero = pygame.transform.rotate(self.imgHero,180)
                            tacticalMap.blit(self.imgHero,[i*tSize+tSize//4-adjI,j*tSize+tSize//4-adjJ])
                        if gameModel.player.f==3: #W
                            fx=-1
                            fy=0
                            rotHero = pygame.transform.rotate(self.imgHero,90)
                            tacticalMap.blit(self.imgHero,[i*tSize+tSize//4-adjI,j*tSize+tSize//4-adjJ])
                        pygame.draw.circle(tacticalMap,(RED),(i*tSize-adjI+tSize//2+fx*25,j*tSize-adjJ+tSize//2+fy*25),tSize//16)
                else:
                    pygame.draw.rect(tacticalMap,(BLACK),(i*tSize-adjI,j*tSize-adjJ,tSize-1,tSize-1))

        self.screen.blit(tacticalMap, (margin,margin))
        pygame.display.update()
