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
from math import radians, cos, sin, asin, sqrt



#global firstTime
#firstTime = 0


class NavyUnit():
    def __init__(self, location, range):
        self.Location = location
        self.Range = range

class ArmyUnit():
    def __init__(self, location, range):
        self.Location = location
        self.Range = range

class AirForceBase():
    def __init__(self, location):
        self.Location = location

class Location():
    def __init__(self,latt,long):
        self.latt = float(latt)
        self.long = float(long)

class Target():
    def __init__(self, location, mobile):
        self.Location = location
        self.Mobile = mobile
        self.Destroyed = False
        self.MunitionUsed = None
        self.PopDensity = None
        self.whoDestroyed = None


class Solution():
    def __init__(self):
        self.Targets = []
        self.score = None


class Scenario():
    def __init__(self, targets, airforcebases, armyunits, navyunits):
        self.Targets = targets
        self.AirForceBases = airforcebases
        self.ArmyUnits = armyunits
        self.NavyUnits = navyunits
        self.Solution = None



def haversine(Location1, Location2):
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
    AFBases = [loc1]

    # Alabama Area
    loc2 = Location(32.31507, -91.59368)
    army1 = ArmyUnit(loc2, 804.0)

    #Gulf Coast
    loc3 = Location(28.11787, -95.37432)
    navy1 = NavyUnit(loc3, 1126.0)

    #Dallas Targets
    loc4 = Location(32.7584072, -96.7359924)
    loc5 = Location(33.7584072, -95.7359924)
    loc6 = Location(31.7584072, -97.7359924)
    target1 = Target(loc4, False)
    target2 = Target(loc5, False)
    target3 = Target(loc6, False)


    #Initialize and Load Scenario from files
    world =  Scenario([target1, target2,target3], [AFBases], [army1], [navy1])

    #Run Simulation
    world.runSim()

    #Evaluate Solution
    world.evaluateSolution

    #loop for improvement








if __name__ == '__main__':
    main()