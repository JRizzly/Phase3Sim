import requests
import pprint
import json
import time
import datetime
import pprint
import sys
import urllib
import urllib2
import json
import time
import datetime
import hmac, hashlib
import datetime
import time
import re
import os.path
import random
from math import radians, cos, sin, asin, sqrt



#global firstTime
#firstTime = 0


'''class NavyUnit():
    def __init__(self, location, range):
        self.Location = location
        self.Range = range'''

class Unit():
    def __init__(self, location, range, type, name):
        self.Location = location
        self.Range = range
        self.Type = type
        self.Name = name
        self.Alive = True
        self.Dead = False

    def printt(self):
        print "   Unit: " + str(self.Name)
        self.Location.printt()
        print "   Range: " + str(self.Range)
        if type == 1:
            print "   Air Force"
        if type == 2:
            print "   Army"
        if type == 3:
            print "   Navy"
        print ""

'''class AirForceBase():
    def __init__(self, location):
        self.Location = location'''

class Location():
    def __init__(self,latt,long):
        self.Latt = float(latt)
        self.Long = float(long)

    '''def __init__(self, location):
        self.latt = location.latt
        self.long = location.long'''

    def printt(self):
        print "      Lattitude: " + str(self.Latt) + "Longitude: " + str(self.Long)


class Target():
    def __init__(self, location, mobile):
        self.Location = Location(location.Latt, location.Long)
        self.Mobile = mobile
        self.Destroyed = False
        self.MunitionUsed = None
        self.PopDensity = None
        self.whoDestroyed = None
        self.inRangeof = []

    def printt(self):
        print "Target Location: " + str(self.Location.Latt) + " " + str(self.Location.Long)
        #self.Location.printt()
        print "Stats: "
        print "   Mobile: " + str(self.Mobile)
        print "   Destroyed: " + str(self.Destroyed)
        print "In Range of: "
        for i in range(0, len(self.inRangeof)):
            self.inRangeof[i].printt()
        print "Who Destoryed Target: " + str(self.whoDestroyed.printt())





class Solution():
    def __init__(self):
        self.Targets = []
        self.score = None


class Scenario():
    def __init__(self, targets, units):
        self.Targets = targets
        self.Units = units
        self.Solution = None

    def findRandomAirForceUnitLocation(self):
        found = False
        iter = 0
        while found == False:
            iter = iter +1
            randAFUnit = random.randint(0,len(self.Units)-1)
            if self.Units[randAFUnit].Type == 1 and self.Units[randAFUnit].Dead == False :
                return randAFUnit
            if iter > 99999:
                print "Stuck in Finding Air Force Loop"

    def findRandomUnitLocation(self):
        found = False
        iter = 0
        while found == False:
            iter = iter +1
            randUnit = random.randint(0,len(self.Units)-1)
            if self.Units[randUnit].Dead == False :
                return randUnit
            if iter > 99999:
                print "Stuck in Finding a Unit"



    def runSim(self):

        #update all targets with units they can be hit by
        for t in range(0, len(self.Targets)):

            for i in range(0, len(self.Units)):
                if distance(self.Targets[t].Location, self.Units[i].Location) < self.Units[i].Range :
                    self.Targets[t].inRangeof.append(self.Units[i])

            #print self.Targets[t].printt()


        #first time - Random assignment
        for t in range(0, len(self.Targets)):

            #for all targets
            for i in range(0, len( self.Targets[t].inRangeof )):
                #if Mobile Target Assign Random Air Force Unit
                if self.Targets[t].Mobile == True and self.Targets[t].Destroyed == False :
                    self.Targets[t].whoDestroyed = self.Units[self.findRandomAirForceUnitLocation()]
                    self.Targets[t].Destroyed = True

                #assign random Unit to destroy target
                if self.Targets[t].Destroyed == False:
                    self.Targets[t].whoDestroyed = self.Units[self.findRandomUnitLocation()]
                    self.Targets[t].Destroyed = True


        #Not first - alter Combinations

            print self.Targets[t].printt()




def distance(Location1, Location2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1 = float(0.00)
    lat1 = float(0.00)
    lon2 = float(0.00)
    lat2 = float(0.00)
    Location1.long = lon1
    Location1.lat = lat1
    Location2.long = lon2
    Location2.lat = lat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 6371 km is the radius of the Earth
    km = 6371 * c
    return km




def main():
    #Read in from files
    #f = open('OfficialRates2.csv', 'a', 0)

    #Colorado SPrings
    loc1 = Location(38.8058, -104.7008)
    unit1 = Unit(loc1,999999,1, "AFJohnny")

    # Alabama Area
    loc2 = Location(32.31507, -91.59368)
    unit2 = Unit(loc2, 804.0, 2, "Army Bob")

    #Gulf Coast
    loc3 = Location(28.11787, -95.37432)
    unit3 = Unit(loc3, 1126.0, 3, "Navy Ned")

    #Dallas Targets
    loc4 = Location(32.7584072, -96.7359924)
    loc5 = Location(33.7584072, -95.7359924)
    loc6 = Location(31.7584072, -97.7359924)
    target1 = Target(loc4, False)
    target2 = Target(loc5, False)
    target3 = Target(loc6, False)


    #Initialize and Load Scenario from files
    world =  Scenario([target1, target2,target3], [unit1, unit2, unit3])

    #Run Simulation
    world.runSim()

    #Evaluate Solution
    #world.evaluateSolution

    #loop for improvement








if __name__ == '__main__':
    main()