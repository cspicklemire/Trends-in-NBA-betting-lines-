note: This project is a work-in-progress

The goal of this project is to learn about the ways to forecast basketball games. Since the most widely accepted forecasts are run by sportsbooks, it made the most sense to me to start the investigation by examining trends in betting lines. There are huge caches of this data readily available, and for the purpose of this project I will be using data sourced from 

https://www.sportsbookreviewsonline.com/scoresoddsarchives/nba/nbaoddsarchives.htm


This great site has complete game summaries, including the opening, closing, and 2nd-half betting lines for every NBA game dating back to the 2007-08 season.

To understand the basics of how betting lines can inform forecasting, there are two main terms that would be helpful to understand:

**Point Spread** - Often referred to simply as "the spread", this tells us how many points the favorite is favored by. The spread is standardized such that each side of the bet is given the same odds, or each side of the wager is balanced to be roughly 50-50. An easy way to think about it is to subtract the point spread from the favorite's total at the end of the game and pay out the bet based on that. Therefore, a point spread of 5.5 means that betting on the favorite pays out if the favorite wins by at least 6, and betting on the underdog pays out so long as they lose by 5 or less. There is not an easy formula to find the implied win percentage from a given point spread, which was one of the curiosities that led me to pursue this project.

**Moneyline** - The moneyline gives the straight-up odds of each team's chance to win the game.

Negative Moneyline - Traditionally assigned to the favorite, tells us how much a bettor would have to put up to win $100. 

Positive Moneyline - Traditionally assigned to the underdog, tells us how much a $100 bet pays out. 

Moneyline bets are NOT standardized to give even sides like spread bets are, and the implied odds can be found by dividing the moneyline by 100. For example, a moneyline of -200 implies odds of 2-to-1 against, while a moneyline of +400 implies 4-to-1 odds in favor of the bettor.

The button below this links to an interactive Jupyter notebook with my code

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cspicklemire/Trends-in-NBA-betting-lines/master)
