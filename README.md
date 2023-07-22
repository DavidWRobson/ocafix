# ocafix

## Introduction

ocafix is a tool to schedule OCA fixtures.  After the initial parameters are defined, it then performs
Monte-Carlo simulations until it finds a fixture list that meets the constraints.  The fixtures are
then written to stdout.  A python pickle file (fixtures.pickle) is also created so that further analysis
can be undertaken.

The code is written in Python3 and uses standard libraries.

## Running Instructions

### On a local machine

Check out this repository and change directory to its contents,  Then run

                              python3 ocafix.py  N
                              
where N is the number of simulations to be evaluated.

### In a web browser

Note that this is unlikely to work as the tight constraints require too larger execution team available at mybinder

Go to https://mybinder.org/v2/gh/DavidWRobson/ocafix/master

Click on the ocafix.ipynb link

Click on the area saying "run -i 'ocafix.py'"  This will make sure it is highlighted (there will be a coloured line on the side), and then just click "Run"  The numerical argument is the number of simulations to be evaluated.

## Current constraints

1. Fixtures lie with the two halves of the season
2. Fixtures occur on the club night of the home team
3. Fixtures are only between teams in the same division
4. Teams in the same division play each other twice; once at home and once away
5. Teams do not play each other twice during the same half of the season
6. Teams from the same club play each other at the beginning of the season halves
7. No team plays more than one match in the same week (except for the University)
8. No fixtures scheduled for the day after Kidlington
9. No fixtures scheduled for the day after The Witney Congress
10. No fixtures scheduled for Easter Bank Holiday
11. No fixtures scheduled for the day of the Cowley Blitz
12. Fixtures between teams from the same club are scheduled as near to the begining of each half of the season as possible
13. No matches to be scheduled outside ranges specified for clubs. Currently MCS, Abingdon School terms and University terms, excluding Michaelmas 1st week for initial preparation and Trinity 5th to 8th week for exams.
14. Clubs do not have more than a specified number of fixtures at home on the same day (currently 2 for most clubs)
15. Cowley does not have more than 1 fixtures at home on the third Monday of the month to avoid clash with Stamp Club.
16. The number of teams that have adjacent teams playing on the same night is minimized.
17. The number of times both Bicester teams play at home on the same night is maximize
18. Cowley Didcot and Witney teams don't have "adjacent" (e.g. Team N and Team N+1) playing on the same night.

## Conversion to a Windows executable

The python program can be built as a standalone windows executable by running the following steps on a Windows machine.  Tested on a Windows 10 machine, will probably work on other versions, also Linux and Mac.

1.  Install PyInstaller with "pip install PyInstaller"
2.  Convert with pyinstaller.exe -F ocafix.py   (builds ocafix.exe in dist folder)
3.  Run with ".\dist\ocafix\ocafix.exe"
