__author__ = 'DWA'

class Connector(object):
    def __init__(self,id,x,y,reg1,reg2,type):
        self.id=id
        self.x=x
        self.y=y
        self.reg1=reg1
        self.reg2=reg2
        self.type=type

    def printConnStatsAsCLI(self):
        print("ID  :"+str(self.id))
        print("X   :"+str(self.x))
        print("Y   :"+str(self.y))
        print("REG1:"+str(self.reg1))
        print("REG2:"+str(self.reg2))
        print("TYPE:"+str(self.type))
        print("")