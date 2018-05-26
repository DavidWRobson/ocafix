#!/usr/bin/env python3

from datetime import date,timedelta
import pickle
import random
import sys


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
['witney',4,0],
['Bicester',2,0],
['Wantage',2,0],
['Cowley',6,3],
],

]

# Weeks with the following days in them will be excluded from fixtures

excludedWeeks = [
date(2019,4,1).isocalendar()[1],
date(2019,4,8).isocalendar()[1],
date(2019,4,15).isocalendar()[1],
date(2019,4,22).isocalendar()[1],
]

firstDateOfFirstHalf=date(2018,10,1)
lastDateOfFirstHalf=date(2018,12,21)
firstDateOfSecondHalf=date(2019,1,7)
lastDateOfSecondHalf=date(2019,5,30)

fixtures = []
fixtureDate = {}  # key is homeClub.HomeTeamNumber.awayClub.awayTeamNumber

#---------------------------------------------------------------------------------------

def isFixtureOK ( pdate, pdivision, phomeClub, phomeTeamNumber, pawayClub, pawayTeamNumber,phomeClubNight):

    pweek = pdate.isocalendar()[1]

    if pweek in excludedWeeks:
       return False

    for fixture in fixtures:
        fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
        fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]
        
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
   random.shuffle(fixtures)

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
             for attempt in range(1,30):
                candidateDate = firstDateOfHalf + timedelta((homeClubNight - firstDayOfHalf) % 7)
                if homeClub != awayClub: 
                   randomWeekShift = 7 * int(random.randint(0,seasonLength - 7) / 7)    # Add a random shift of a whole number of weeks
                   candidateDate += timedelta(randomWeekShift)
                fixtureOK = isFixtureOK ( candidateDate, fdiv, homeClub, homeTeamNumber, awayClub, awayTeamNumber,homeClubNight )
                if fixtureOK:
                   break 
             if not fixtureOK:
                return False
        
             fixtureDate[homeClub + str(homeTeamNumber) + awayClub + str(awayTeamNumber)] = candidateDate

   return True

#---------------------------------------------------------------------------------------

def main():
    for j in range(0,300):
        fillFixtures()
        itWorked = attemptFixtures()
        if itWorked:
           break
    if itWorked:
       for fixture in fixtures:
           fdiv, fhomeClub, fhomeTeamNumber, fawayClub, fawayTeamNumber,fhomeClubNight = fixture
           fdate = fixtureDate[fhomeClub + str(fhomeTeamNumber) + fawayClub + str(fawayTeamNumber)]
           print(fdate.strftime('%Y-%m-%d (%a)')+" "+fdiv+" "+fhomeClub+str(fhomeTeamNumber)+" v "+fawayClub + str(fawayTeamNumber))
       pickle.dump( [fixtures,fixtureDate] , open( "fixtures.pick", "wb" ) )
    else:
       print("Failed to find a solution",file=sys.stderr)

#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()