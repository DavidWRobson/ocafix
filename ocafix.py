#!/usr/bin/env python3

#######################################################################
# Author David.Robson
# 2018-05-24 Created
#
# The number of simulations to be undertaken is supplied by an argument.
# The default is one.
#######################################################################

from datetime import date,timedelta
import pickle
import random
import sys

maxConcurrentHomeMatchesPerClub = {

'University' : 2,
'Witney'     : 2,
'City'       : 2,
'Cowley'     : 3,
'Banbury'    : 2,
'Didcot'     : 2,
'Bicester'   : 2,
'Wantage'    : 2,
'Cumnor'     : 2,
'MCS/B'      : 2,
'Abingdon'   : 2,

}

Monday    = 0
Tuesday   = 1
Wednesday = 2
Thursday  = 3

# Club,TeamNumber,Division,Match Night (Monday=0)

teams = [    

# Division 1
[
['University', 1, Thursday],
['Witney',     1, Monday],
['City',       1, Monday],
['Cowley',     2, Thursday],
['Witney',     2, Monday],
['Banbury',    1, Thursday],
['Cowley',     1, Monday],
['Cumnor',     1, Thursday],
],

# Division 2

[
['Bicester',   1, Tuesday],
['University', 2, Thursday],
['Banbury',    2, Thursday],
['Wantage',    1, Tuesday],
['City',       2, Monday],
['Cowley',     3, Monday],
['Didcot',     1, Wednesday],
['Didcot',     2, Monday],
],

# Division 3

[
['Didcot',     3, Wednesday],
['Banbury',    3, Thursday],
['City',       3, Monday],
['Cowley',     4, Thursday],
['Witney',     3, Monday],
['Cowley',     5, Monday],
['Abingdon',   1, Monday],
],

# Division 4

[
['Didcot',     4, Monday],
['University', 3, Thursday],
['Witney',     4, Monday],
['Bicester',   2, Tuesday],
['Wantage',    2, Tuesday],
['Cowley',     6, Thursday],
['Cumnor',     2, Thursday],
],

]

# Following clubs will be scheduled as early in the season as possible

clubsForEarlyScheduling = [
'University'
]

# Following clubs hve expressed desire that they don't have adjacent teams (e.g. team N and team N+1) playing on the same night.

#adjacentIssueClubs = ['Witney', 'Didcot', 'Cowley']

adjacentIssueClubs = ['Witney', 'Didcot','Cowley']

# Following days will be excluded from fixtures for everyone

globalExcludedDays = [
date(2020,4,20),       # Peter Wells' Simultaneous
date(2020,2,3),        # Kidlington Tournament Hangover
date(2019,11,4),       # Witney Weekend Congress Hangover
date(2020,4,10),       # Good Friday
date(2020,4,13),       # Easter Bank Holiday 
date(2020,6,8),        # Cowley Blitz 
]

# Following days will be excluded from fixtures for specific teams
teamExcludedDays = {
    
  'Cowley2'     : [
      date(2020,4,9),  # Maunday Thursday
   ],
 }

availablePeriods = {

'Abingdon' : [
[ date(2019,9,3), date(2019,10,11) ],     # Michaelmas 1st half
[ date(2019,10,28), date(2019,12,13) ],   # Michaelmas 2nd half
[ date(2020,1,7), date(2020,2,14) ],      # Lent 1st half
[ date(2020,2,24), date(2020,3,27) ],     # Lent 2nd half
[ date(2020,4,21), date(2020,5,22) ],     # Summer 1st half
[ date(2020,6,1), date(2020,7,3) ],       # Summer 2nd half
],

'University' : [
[ date(2019,10,14), date(2019,12,6) ],    # Michaelmas:  2nd to 7th week
[ date(2020,1,20), date(2020,3,13) ],     # Hilary:      1st to 8th week
[ date(2020,4,27), date(2020,5,19) ],     # Trinity:     1st to 4th week
],

}

# Weeks with the following days in them will be excluded from fixtures for everyone

globalExcludedWeeks = [
#date(2020,4,6).isocalendar()[1],
date(2020,12,1).isocalendar()[1],
]

# Define the two halves of the season

firstDateOfFirstHalf=date(2019,9,30)
lastDateOfFirstHalf=date(2019,12,13)

firstDateOfSecondHalf=date(2020,1,6)
lastDateOfSecondHalf=date(2020,5,1)

bestScore = 99999

fixtures = []
fixtureDate = {}  # key is homeClub.HomeTeamNumber.awayClub.awayTeamNumber

#---------------------------------------------------------------------------------------

def isFixtureOK ( pdate, pdivision, phomeClub, phomeTeamNumber, pawayClub, pawayTeamNumber,phomeClubNight):

    pweek = pdate.isocalendar()[1]
    homeFixturesOnThisDay = 0

# Check that proposed fixture is not an excluded day

    if pdate in globalExcludedDays:
       return False

# Check that proposed fixture is not in an excluded week

    if pweek in globalExcludedWeeks:
       return False

# Check that home team is playing in a their allowed period

    inAllowedPeriod = False
    try:
        for period in availablePeriods[phomeClub]:
            start, finish = period
            if start <= pdate <= finish:
               inAllowedPeriod = True
    except KeyError:
       inAllowedPeriod = True        # No list of allowed periods so assume all dates possible
    if not inAllowedPeriod:
       return False

# Check that away team is playing in their allowed period

    inAllowedPeriod = False
    try:
        for period in availablePeriods[pawayClub]:
            start, finish = period
            if start <= pdate <= finish:
               inAllowedPeriod = True
    except KeyError:
       inAllowedPeriod = True        # No list of allowed periods so assume all dates possible
    if not inAllowedPeriod:
       return False
    

# Check if date is excluded for the home team

    try:
        for excludedDate in teamExcludedDays[phomeClub + str(phomeTeamNumber)]:
            if pdate == excludedDate:
               return False
    except KeyError:
        pass

# Check if date is excluded for the away team

    try:
        for excludedDate in teamExcludedDays[pawayClub + str(pawayTeamNumber)]:
            if pdate == excludedDate:
               return False
    except KeyError:
        pass

    bicester1AtHomeOnThisDay  = False

    for fixture in fixtures:
        fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
        fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]

        if fhomeClub == phomeClub and fdate == pdate:
           homeFixturesOnThisDay += 1

# Check that the home club isn't exceeding its maximum number of fixtures per night
        
           try:
              if homeFixturesOnThisDay >= maxConcurrentHomeMatchesPerClub[phomeClub]:
                 return False
           except KeyError:
               print("No maxConcurrentHomeMatchesPerClub for",phomeClub,file=sys.stderr)
               sys.exit(2)

# Check that there isn't already a Cowley home fixtures on this day
# if it is the third Monday of the week (Stamp Club clash)
        
           if phomeClub == 'Cowley' and 14 < pdate.day < 22 and homeFixturesOnThisDay >= 1:
              return False

        if fdate is not None:    # i.e. a fixture has already been scheduled


#--------------------------------------------------
#          Examine fixtures happening in this week
#--------------------------------------------------

           fweek = fdate.isocalendar()[1]
           if pweek == fweek:

# Check if proposed home team already has a home fixture in this week
# Exclude the University, because of their short terms
        
              if phomeClub == fhomeClub and phomeClub != 'University' and phomeTeamNumber == fhomeTeamNumber:
                 return False

# Check if proposed home team already has a away fixture in this week
# Exclude the University, because of their short terms
        
              if phomeClub == fawayClub and phomeClub != 'University' and phomeTeamNumber == fawayTeamNumber:
                 return False

# Check if proposed away team already has a home fixture in this week
# Exclude the University, because of their short terms
        
              if pawayClub == fhomeClub and pawayClub != 'University' and pawayTeamNumber == fhomeTeamNumber:
                 return False

# Check if proposed away team already has an away fixture in this week
# Exclude the University, because of their short terms
        
              if pawayClub == fawayClub and pawayClub != 'University' and pawayTeamNumber == fawayTeamNumber:
                 return False

#--------------------------------------------------
#          Examine fixtures happening on this day
#--------------------------------------------------

           if pdate == fdate:

# Check if home team already has a home fixture on this day
        
              if (phomeClub == fhomeClub and phomeTeamNumber == fhomeTeamNumber) or phomeClub == fawayClub and phomeTeamNumber == fawayTeamNumber:
                 return False

# Check if away team already has a home fixture on this day
        
              if (pawayClub == fhomeClub and pawayTeamNumber == fhomeTeamNumber) or pawayClub == fawayClub and pawayTeamNumber == fawayTeamNumber:
                 return False

# Ensure that adjacent teams (for clubs who have expressed such a prfeference), don't play on the same night
# Note, it doesn't look possible to do this for all clubs

              if  phomeClub in adjacentIssueClubs:

                 if phomeClub == fhomeClub and abs( phomeTeamNumber - fhomeTeamNumber ) == 1:
                    return False

                 if phomeClub == fawayClub and abs( phomeTeamNumber - fawayTeamNumber ) == 1:
                    return False

              if  pawayClub in adjacentIssueClubs:

                 if pawayClub == fhomeClub and abs( pawayTeamNumber - fhomeTeamNumber ) == 1:
                    return False

                 if pawayClub == fawayClub and abs( pawayTeamNumber - fawayTeamNumber ) == 1:
                    return False

    return True

#---------------------------------------------------------------------------------------

def fillFixtures():

   fixtures.clear()

   # Generate required fixtures

   for division in range(0,len(teams)):
      for homeTeam in teams[division]:
          homeClub, homeTeamNumber, homeTeamNight = homeTeam
          for awayTeam in teams[division]:
              awayClub, awayTeamNumber, awayTeamNight = awayTeam
              if homeClub != awayClub or homeTeamNumber != awayTeamNumber: # teams cannot play themselves
                 awayClub, awayTeamNumber, awayTeamNight = awayTeam
                 fixture = ["Div" + str(division + 1), homeClub, homeTeamNumber, awayClub, awayTeamNumber, homeTeamNight]
                 fixtures.append(fixture)
                 fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)] = None

#  Randomize the order so that the next iteration will be different

   random.shuffle(fixtures)

# If the fixture is between two teams from the same club, put them at the beginning
# of the list so that they can be scheduled for the start of the season halves.

# Find the inter-club fixtures

   interClubFixtures = []
   for fixture in fixtures:
       fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
       if homeClub == awayClub:
          interClubFixtures.append(fixture)

# Then put the inter-club fixtures at the top of the fixture list

   for fixture in interClubFixtures:
       fixtures.remove(fixture)
       fixtures.insert(0, fixture)

#---------------------------------------------------------------------------------------

def attemptFixtures():

   # Clear old fixture dates

   for key,value in fixtureDate.items():
       fixtureDate[key] = None

   # Generate fixture dates

   for division in range(0,len(teams)):
      for fixture in fixtures:
          fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
          fdate = fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)]

          if fdate is None:
            # If return match already scheduled, schedule this one in the second half
             if  fixtureDate[awayClub + str(awayTeamNumber) + homeClub + str(homeTeamNumber)] is None:
                 firstDateOfHalf = firstDateOfFirstHalf
                 lastDateofHalf = lastDateOfFirstHalf
             # Otherwise schedule this in the first half
             else:
                 firstDateOfHalf = firstDateOfSecondHalf
                 lastDateofHalf = lastDateOfSecondHalf
             firstDayOfHalf = date.weekday(firstDateOfHalf)
             seasonLength = (lastDateofHalf - firstDateOfHalf).days

             fixtureOK = False;

# Try random dates in an attempt to spread the fixtures evenly through the available times

             if not fixtureOK:
                for attempt in range(0,150):
                   candidateDate = firstDateOfHalf + timedelta((homeClubNight - firstDayOfHalf) % 7)
                   if homeClub != awayClub: 
                      # Add a random shift of a whole number of weeks
                      randomWeekShift = 7 * int(random.randint(0,seasonLength - 7) / 7) 
                      candidateDate += timedelta(randomWeekShift)

                   fixtureOK = isFixtureOK ( candidateDate, fdiv, homeClub, homeTeamNumber, awayClub, \
                                             awayTeamNumber,homeClubNight )
                   if fixtureOK:
                      break 
                if not fixtureOK:
                   return False
        
             fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)] = candidateDate

   return True

#---------------------------------------------------------------------------------------

def scoreSimulation():

    score = 0

    for fixture in fixtures:
        div, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
        fdate = fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)]


        for lfixture in fixtures:

            ldiv, lhomeClub, lhomeTeamNumber, lawayClub, lawayTeamNumber,lhomeClubNight = lfixture
            ldate = fixtureDate[lhomeClub + str(lhomeTeamNumber) + lawayClub + str(lawayTeamNumber)]

            scoreForHomeTeamThisFixture = scoreForAwayTeamThisFixture = 0

            if fdate == ldate:

# Increase score if home team already has an adjacent team playing on this day

               if homeClub == lhomeClub and abs( homeTeamNumber - lhomeTeamNumber ) == 1:
                  scoreForHomeTeamThisFixture =  scoreForHomeTeamThisFixture * 3 + 1

               if homeClub == lawayClub and abs( homeTeamNumber - lawayTeamNumber ) == 1:
                  scoreForHomeTeamThisFixture =  scoreForHomeTeamThisFixture * 3 + 1


# Increase score if away team already has an adjacent team playing on this day

               if awayClub == lhomeClub and abs( awayTeamNumber - lhomeTeamNumber ) == 1:
                  scoreForAwayTeamThisFixture =  scoreForAwayTeamThisFixture * 3 + 1

               if awayClub == lawayClub and abs( awayTeamNumber - lawayTeamNumber ) == 1:
                  scoreForAwayTeamThisFixture =  scoreForAwayTeamThisFixture * 3 + 1

# Decrease score if Bicester teams are playing home matches on the same day

               if homeClub == 'Bicester' and lhomeClub == 'Bicester' and homeTeamNumber != lhomeTeamNumber:
                  score -= 10

            score += scoreForHomeTeamThisFixture + scoreForAwayTeamThisFixture

    return score

#---------------------------------------------------------------------------------------

def trySimulation(count):

   global bestScore

   for j in range(0,10000):
       fillFixtures()
       itWorked = attemptFixtures()
       if itWorked:
          break

   if itWorked:
      score = scoreSimulation()
      if score < bestScore:
         bestScore = score
         pickle.dump( [fixtures,fixtureDate] , open( "fixtures.pickle", "wb" ) )

   if itWorked:
      return True
   return False

#---------------------------------------------------------------------------------------

def printFixtureList():

    try:
        data = pickle.load(open( "fixtures.pickle", "rb" ))
        fixtures, fixtureDate = data

        outputs = []
        for fixture in fixtures:
            fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
            fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]
            outputs.append(fdate.strftime('%Y-%m-%d (%a)') +" " + fdiv + " " + \
                    '{0: <12}'.format(fhomeClub + " " + str(fhomeTeamNumber))  + " v " + \
                    '{0: <12}'.format(fawayClub + " " + str(fawayTeamNumber)))

        outputs.sort()
        for output in outputs:
            print(output)
    except FileNotFoundError:
        print("ERROR: Pickle file not found",file=sys.stderr)
        pass

#---------------------------------------------------------------------------------------

def main(argv):

       numberOfSimulations = 50
       if len(argv) > 1:
          try:
             numberOfSimulations = int(argv[1])
          except ValueError:
             print ("Argument", argv[1], "is not a valid number of simulations", file=sys.stderr)
             sys.exit(2)
       
       solutionFound = False
       for j in range(0, numberOfSimulations):
           if trySimulation(j):
              solutionFound = True

       if solutionFound:
          printFixtureList()
          sys.exit(0)

       else:
          print("Unable to find a solution",file=sys.stderr)
          sys.exit(1)

#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main( sys.argv)
