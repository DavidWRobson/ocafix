# ocafix

ocafix is a tool to schedule OCA fixtures.  After the initial parameters are defined, it then performs
Monte-Carlo simulations until it finds a fixture list that meets the constraints.  The fixtures are
then written out to stdout.  A python "pickle" file is also created so that further analysis can be
undertaken.

## Current constraints

1. Fixtures lie with the two halves of the season
2. Fixtures occur on the club night of the home team
3. Fixtures are only between teams in the same division
4. Teams in the same division play each other twice; once at home and once away
5. Teams do not play each other twice during the same half of the season
6. No team plays more than one match in the same week
7. No fixtures scheduled for the day after Kidlington
8. No fixtures scheduled for the day of the Peter Well's simultaneous event
9. All University matches are scheduled in term time                                   - YET TO BE DONE
10. Cowley does not have more than 3 fixtures at home on the same day                  - YET TO BE DONE
11. Cowley does not have more than 1 fixtures at home on the third Monday of the month - YET TO BE DONE
