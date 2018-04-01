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
import copy
import random
from math import radians, cos, sin, asin, sqrt

global inf
inf = 999999999.9

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
        if self.Type == 1:
            print "   Type: Air Force"
        if self.Type == 2:
            print "   Type: Army"
        if self.Type == 3:
            print "   Type: Navy"
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
        print "      Lattitude: " + str(self.Latt) + " Longitude: " + str(self.Long)


class Munition():
    def __init__(self, name, platform, cost, range, cep, reliability, quantity, blastRadius):
        self.Name = name
        self.Platform   = platform
        self.Cost = cost
        self.Range = range
        self.Cep = cep
        self.Reliability = reliability
        self.Quantity = quantity
        self.BlastRadius = blastRadius




class Target():
    def __init__(self, location, mobile):
        self.Location = Location(location.Latt, location.Long)
        self.Mobile = mobile
        self.Destroyed = False
        self.PopDensity = None
        self.whoAssigned = None
        self.Assigned = False
        self.inRangeof = []

        #for quantifying effectiveness
        #operational Effectiveness
        self.NumAirCraftLost = 0.0
        self.MunitionsUsed = []

             #Cost of Stategy
        self.MunitionCost = 0.0
        self.DownedAirCraftCost = 0.0

        #Collateral Damage
        self.NumOfCasulties = 0.0



    def printt(self):
        print "Target Location: " + str(self.Location.Latt) + " " + str(self.Location.Long)
        #self.Location.printt()
        print "Stats: "
        print "   Mobile: " + str(self.Mobile)
        print "   Destroyed: " + str(self.Destroyed)
        print "In Range of: "
        for i in range(0, len(self.inRangeof)):
            self.inRangeof[i].printt()
        print "Who Assigned to Target: "
        print self.whoAssigned.printt()


class Solution():
    def __init__(self, targets):
        #array of destroyed targets
        self.Targets = targets

        # ------------- Totals -------
        #Ops Effectivness
        self.TotNumAirCraftLost = 0.0
        self.TotMunitionsUsed = []
        #Cost
        self.TotMunitionCost = 0.0
        self.TotDownedAirCraftCost = 0.0
        #Collateral Damage
        self.TotNumOfCasualties = 0.0

        #------------- Scores -------------------
        self.OperationalEffectivenessScore = 0.0
        self.CostScore = 0.0
        self.CollateralDamageScore = 0.0
        self.TotalScore = 0.0
        self.WeightedScore = 0.0

    def calculateScore(self):
        for t in range(0, len(self.Targets)):
            self.TotNumAirCraftLost = self.TotNumAirCraftLost + self.Targets[t].NumAirCraftLost
            self.TotMunitionsUsed = self.TotMunitionsUsed + self.Targets[t].MunitionsUsed
            self.TotMunitionCost += self.Targets[t].MunitionCost
            self.TotDownedAirCraftCost += self.Targets[t].DownedAirCraftCost
            self.TotNumOfCasualties += self.Targets[t].NumOfCasulties

        #Building Scores
        # I think we also need to assign weighting to the factors which make up a MOM
        #Right now it weights the use of 1 munition the same as the loss of an aircraft
        self.OperationalEffectivenessScore = self.TotNumAirCraftLost + len( self.TotMunitionsUsed )
        self.CostScore = self.TotMunitionCost + self.TotDownedAirCraftCost
        self.CollateralDamageScore = self.TotNumOfCasualties

        #TODO: make low cost better the score simple subtraction right now
        self.TotalScore = self.OperationalEffectivenessScore*float(.55) - self.CostScore*float(.1) + self.CollateralDamageScore*float(.35)
        self.WeightedScore = self.TotalScore/len(self.Targets)

        print "Total Cost: " + str(self.TotMunitionCost)



class Family():
    def __init__(self):
        self.children = []


class Scenario():
    def __init__(self, targets, units, munitions, age):
        self.Targets = targets
        self.Units = units
        self.Munitions = munitions
        self.Solution = None
        self.SolutionSets = []
        self.Age = age
        self.PreviousCleanTargetState = None

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

        #find for assignment
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


    def firstTimeRandomAssignments(self):
        #for all targets
        for t in range(0, len(self.Targets)):

            #for all units in range of this target
            for i in range(0, len( self.Targets[t].inRangeof )):

                #if Mobile Target then Assign Random Air Force Unit
                if self.Targets[t].Mobile == True and self.Targets[t].Assigned == False :
                    self.Targets[t].whoAssigned = self.Units[self.findRandomAirForceUnitLocation()]
                    self.Targets[t].Assigned = True

                #assign random Unit to  target
                if self.Targets[t].Assigned == False:
                    self.Targets[t].whoAssigned = self.Units[self.findRandomUnitLocation()]
                    self.Targets[t].Assigned = True

        #setting Previous state for clean targets with assignemnts
        self.PreviousCleanTargetState = copy.deepcopy(self.Targets)

        for t in range(0, len(self.Targets)):
            print self.Targets[t].printt()




    def AFAttack(self,t):
        #This is where we can perform complex math to figure probabilities for attacking this
        #target at this specific location

        '''Complicated Math here '''

        self.Targets[t].MunitionCost += 1.0




        #It will end with target being destroyed
        self.Targets[t].Destroyed = True
        self.MunitionUsed = "Munition that best fits our equation"

    def ArmyAttack(self,t):
        #This is where we can perform complex math to figure probabilities for attacking this
        #target at this specific location

        '''Complicated Math here '''

        self.Targets[t].MunitionCost += 10.0

        #It will end with target being destroyed
        self.Targets[t].Destroyed = True
        self.MunitionUsed = "Munition that best fits our equation"

    def NavyAttack(self,t):
        #This is where we can perform complex math to figure probabilities for attacking this
        #target at this specific location

        '''Complicated Math here '''
        self.Targets[t].MunitionCost += 100.0

        #It will end with target being destroyed
        self.Targets[t].Destroyed = True
        self.MunitionUsed = "Munition that best fits our equation"



    def simulateAttacks(self):
        # for all targets
        for t in range(0, len(self.Targets)):
            #attack modeld by type of uint
            if ( self.Targets[t].whoAssigned.Type == 1 ):
                self.AFAttack(t)
            if (self.Targets[t].whoAssigned.Type == 2):
                self.ArmyAttack(t)
            if ( self.Targets[t].whoAssigned.Type == 3 ):
                self.NavyAttack(t)


    def checkAndCalculateScore(self):
        AssignedAndDestroyed = True
        count = 0
        solution1 = Solution(self.Targets)
        for t in range(0, len(self.Targets)):
            if ( self.Targets[t].Assigned == False or self.Targets[t].Destroyed == False  ):
                AssignedAndDestroyed = False
                count += 1

        if ( AssignedAndDestroyed == True  ) :
            solution1.calculateScore()
            self.Solution = copy.deepcopy(solution1)
            self.SolutionSets.append(copy.deepcopy(self.Solution))
        else:
            print "Not All Targets are Assigned or Destoryed: " + str(count ) + " Not Assigned or Destroyed"


    def setFeasibleTargest(self):
        # update all targets with units they can be hit by with respect to unit Grand Range
        for t in range(0, len(self.Targets)):

            for i in range(0, len(self.Units)):
                if distance(self.Targets[t].Location, self.Units[i].Location) < self.Units[i].Range:
                    self.Targets[t].inRangeof.append(self.Units[i])

            # print self.Targets[t].printt()


    def modifyAssignments(self):
        #Randomly change an assignment

        randTarget = random.randint(0, len(self.Targets) - 1)

        # for all units in range of this target
        for i in range(0, len(self.Targets[randTarget].inRangeof)):

            # if Mobile Target then Assign Random Air Force Unit
            if self.Targets[randTarget].Mobile == True:
                self.Targets[randTarget].whoAssigned = self.Units[self.findRandomAirForceUnitLocation()]
                self.Targets[randTarget].Assigned = True

            # assign random Unit to  target
            if self.Targets[randTarget].Assigned == True:
                self.Targets[randTarget].whoAssigned = self.Units[self.findRandomUnitLocation()]
                self.Targets[randTarget].Assigned = True


    def resetToPreviousCleanState(self):
        self.Targets = copy.deepcopy(self.PreviousCleanTargetState)
        self.Solution = None

    def runSim(self):

        #sets Targets based on Grand Ranges
        self.setFeasibleTargest()

        #first time - Random assignment
        self.firstTimeRandomAssignments()

        #setting previous State
        #self.PreviousState = copy.deepcopy(self.Targets)

        #Simulate Attacks
        self.simulateAttacks()

        #Calculate Score after attacks
        self.checkAndCalculateScore()

        for i in range(0, self.Age):
            #Load Previous State
            self.resetToPreviousCleanState()

            #Modify Assignments
            self.modifyAssignments()

            # Simulate Attacks
            self.simulateAttacks()

            # Calculate Score after attacks
            self.checkAndCalculateScore()








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
    global inf
    #Read in from files
    #f = open('OfficialRates2.csv', 'a', 0)

    #Service Assignments
    #1 - air force , 2 is army , 3 is navy

    ###### UNITS #####
    #Colorado SPrings
    loc1 = Location(38.8058, -104.7008)
    unit1 = Unit(loc1,999999,1, "AFJohnny")

    # Alabama Area
    loc2 = Location(32.31507, -91.59368)
    unit2 = Unit(loc2, 804.0, 2, "Army Bob")

    #Gulf Coast
    loc3 = Location(28.11787, -95.37432)
    unit3 = Unit(loc3, 1126.0, 3, "Navy Ned")

    ###### Targets #####
    #Dallas Targets
    loc4 = Location(32.7584072, -96.7359924)
    loc5 = Location(33.7584072, -95.7359924)
    loc6 = Location(31.7584072, -97.7359924)
    target1 = Target(loc4, False)
    target2 = Target(loc5, False)
    target3 = Target(loc6, False)

    ###### Munitions #####
    #Distance all in km and and blast radius in meters
    # def __init__(self, name, platform, cost, range, cep, reliability, quantity, blastRadius):
    mun1 = Munition("GBU-10", 1, 23000.0, inf, 9, .95, inf, 20)
    mun2 = Munition("ATACM Block IVA",2, 820000.0, 300.0, 4.0, .92,96, 100.0)
    mun3 = Munition("USN DDG",3,500000.0,1111.2,12.2,.85,inf, 10)




    #TODO: Handle the case switching assignments in the case of no muni8tions left to be used by that unit

    #Initialize and Load Scenario from files
    grandFamily = Family()
    numKids = 1
    childAge = 3

    #build the number of Children in the family
    for i in range(0, numKids):
        child = Scenario([target1, target2,target3], [unit1, unit2, unit3], [mun1, mun2, mun3], childAge)
        grandFamily.children.append(copy.deepcopy(child))

    #Run evolution of each child
    # seperate thread so it can be multithreaded as needed
    for i in range(0, len(grandFamily.children )):
        grandFamily.children[i].runSim()
        print "End Scenario "
        print ""


    '''
    for i in range(0, children):
        world =  Scenario([target1, target2,target3], [unit1, unit2, unit3], [mun1, mun2, mun3])

    #One Child and Grows
    world.runSim()
    '''









if __name__ == '__main__':
    main()