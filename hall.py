__author__ = 'DWA'

class Hall(object):
    def __init__(self,id):
        self.id=id
        self.crumbs=[]
        self.paths=[]

    def printHallStatsAsCLI(self):
        print("H"+str(self.id))
        print("PATHS:")
        print(self.paths)
        print("")