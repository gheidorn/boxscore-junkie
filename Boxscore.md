## Introduction ##
There is an assumed format that gets tweaked now and then as new stats are popularized, such as On-Base Percentage (OBP) and On-Base Plus Slugging (OPS) in recent years.  This page describes that general "human-readable" format and then the XML/JSON formats provided by MLBAM for the Scoreboard.

## What is a Boxscore? ##
The boxscore refers to the statistics recorded for a particular game.  Usually the format for a boxscore has both hitting lineups (including in-game substitutions) and each hitter's results (AB, R, H, RBI, BB, SO, LOB, AVG).  Then there is traditionally a set of Batting notes, Baserunning notes and Fielding notes to capture more detailed information like doubles, triples, HRs ... SBs and CSs ... and DPs turned, errors.  Following the position player notes there is the pitcher's box, which contains IP, H, R, ER, BB, SO, HR, and ERA.  Rounding out the boxscore is the game notes which highlights rarer occurrences such as HBP, Balks, Wild Pitches, Passed Balls, as well as umpire, weather and attendance information.

## Boxscore XML ##
If you are better versed in reading XSDs, here is the [Boxscore XSD](http://boxscore-junkie.googlecode.com/files/boxscore.xsd) I reverse-engineered using Castor.

XML sample TBD.

## Copyright Information ##
The accounts, descriptions, data and presentation in the referring page (the "Materials") are proprietary content of MLB Advanced Media, L.P ("MLBAM").

Only individual, non-commercial, non-bulk use of the Materials is permitted and any other use of the Materials is prohibited without prior written authorization from MLBAM.

Authorized users of the Materials are prohibited from using the Materials in any commercial manner other than as expressly authorized by MLBAM.

[MLBAM Copyright Notice](http://gd2.mlb.com/components/copyright.txt)