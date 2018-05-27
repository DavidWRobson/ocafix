#!/usr/bin/env python3

from datetime import date,timedelta
import pickle
import random
import sys


maxHomeMatchesPerClub = {

'Oxford University' : 2,
'Witney' : 3,
'City' : 2,
'Cowley' : 2,
'Witney' : 2,
'Banbury' : 2,
'Didcot' : 2,
'Bicester' : 2,
'Wantage' : 2,
'Cumnor' : 2,
'MCS/B' : 3,
'Abingdon' : 2,

}

# Club,TeamNumber,Division,Match Night (Monday=0)

teams = [    

# Divison 1
[
['Oxford University',1,3],
['Witney',1,0],
['City',1,0],
['Cowley',2,3],
['Witney',2,0],
['Banbury',1,1],
['Didcot',1,2],
['Cowley',1,0],
],

# Division 2

[
['Bicester',1,0],
['Oxford University',2,3],
['Banbury',2,1],
['Wantage',1,1],
['Cowley',3,0],
['Cumnor',1,3],
['City',2,0],
['Cowley',4,0],
],

# Division 3

[
['Didcot',2,2],
['MCS/B',1,0],
['Didcot',3,2],
['Banbury',3,2],
['City',3,0],
['Cumnor',2,4],
['Cowley',5,0],
],

# Division 4

[
['Didcot',4,0],
['Oxford University',3,3],
['Abingdon',1,0],
['Witney',4,0],
['Bicester',2,0],
['Wantage',2,0],
['Cowley',6,3],
],

]

# Following days will be excluded from fixtures for everyone

globalExcludedDays = [
date(2019,4,8),        # Peter Well's Simultaneous
date(2019,2,4),        # Kidlington Tournament Hangover
date(2018,11,5),       # Witney Weekend Congress Hangover
date(2019,4,22),       # Easter Bank Holiday 
date(2019,4,22),       # Cowley Blitz 
]

universityTerms = [

[ date(2018,10,7), date(2018,12,1) ],   # Michaelmas
[ date(2019,1,13), date(2019,3,9) ],    # Hilary
[ date(2019,4,28), date(2019,6,22) ],   # Trinity

]

# Weeks with the following days in them will be excluded from fixtures for everyone

globalExcludedWeeks = [
#date(2019,4,1).isocalendar()[1],
#date(2019,4,8).isocalendar()[1],
#date(2019,4,15).isocalendar()[1],
#date(2019,4,22).isocalendar()[1],
]

# Define the two halves of the season

firstDateOfFirstHalf=date(2018,10,8)
lastDateOfFirstHalf=date(2018,12,21)

firstDateOfSecondHalf=date(2019,1,7)
lastDateOfSecondHalf=date(2019,5,30)

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

# Check that University matches are played in term time

    if  phomeClub == 'Oxford University' or pawayClub == 'Oxford University':
           inTermTime = False
           for term in universityTerms:
               start, finish = term
               if start <= pdate <= finish:
                  inTermTime = True
           if not inTermTime:
              return False;

    for fixture in fixtures:
        fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
        fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]

        if fhomeClub == phomeClub and fdate == pdate:
           homeFixturesOnThisDay += 1

# Check that the home club isn't exceeding its maximum number of fixtures per night
        
           try:
              if homeFixturesOnThisDay >= maxHomeMatchesPerClub[phomeClub]:
                 return False
           except KeyError:
               print("No maxHomeMatchesPerClub for",phomeClub,file=sys.stderr)
               sys.exit(2)

# Check that there isn't already a Cowley home fixtures on this day
# if it is the third Monday of the week (Stamp Club clash)
        
           if 14 < pdate.day < 22 and homeFixturesOnThisDay >= 1:
              return False

        if fdate is not None:
           fweek = fdate.isocalendar()[1]

           if pweek == fweek:

# Check if home club already has a home fixture in this week
        
              if phomeClub == fhomeClub and phomeTeamNumber == fhomeTeamNumber:
                 return False

# Check if home club already has a home fixture in this week
        
              if phomeClub == fawayClub and phomeTeamNumber == fawayTeamNumber:
                 return False

# Check if away club already has a home fixture in this week
        
              if pawayClub == fhomeClub and pawayTeamNumber == fhomeTeamNumber:
                 return False

# Check if home club already has a home fixture in this week
        
              if pawayClub == fawayClub and pawayTeamNumber == fawayTeamNumber:
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

# Find the inter club fixtures

   interClubFixtures = []
   for fixture in fixtures:
       fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight = fixture
       if homeClub == awayClub:
          interClubFixtures.append(fixture)

# Then put the inter club fixtures at the top of the fixture list

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
             for attempt in range(1,100):
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

def main():
    for j in range(0,10000):
        fillFixtures()
        itWorked = attemptFixtures()
        if itWorked:
           break
    if itWorked:
       for fixture in fixtures:
           fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
           fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]
           print(fdate.strftime('%Y-%m-%d (%a)') +" " + fdiv + " " + fhomeClub + str(fhomeTeamNumber)\
                  + " v " + fawayClub + str(fawayTeamNumber))
       pickle.dump( [fixtures,fixtureDate] , open( "fixtures.pickle", "wb" ) )
       sys.exit(0)
    else:
       print("Unable to find a solution",file=sys.stderr)
       sys.exit(1)

#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
