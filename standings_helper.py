import logging
import json_helper

class Standings():
  def __init__ (self):
    self
    
class League():
  def __init__ (self, code):
    self.code = code

class Division():
  def __init__ (self, code):
    self.code = code

class TeamStanding():
  def __init__ (self, code):
    self.code = code
    
def getStandings(year, month, day):
    standings = Standings()
    standings.al = League("al")
    standings.al.e = Division("ale")
    standings.al.e.teams = getTeamStandings(year, month, day, "ale")
    standings.al.c = Division("alc")
    standings.al.c.teams = getTeamStandings(year, month, day, "alc")
    standings.al.w = Division("alw")
    standings.al.w.teams = getTeamStandings(year, month, day, "alw")
    
    standings.nl = League("nl")
    standings.nl.e = Division("nle")
    standings.nl.e.teams = getTeamStandings(year, month, day, "nle")
    standings.nl.c = Division("nlc")
    standings.nl.c.teams = getTeamStandings(year, month, day, "nlc")
    standings.nl.w = Division("nlw")
    standings.nl.w.teams = getTeamStandings(year, month, day, "nlw")
    
    return standings
        
def getTeamStandings(year, month, day, division):
    standings = json_helper.fetchStandings(year, month, day, division)
    teams = []
    for i in range(len(standings)):
      if standings[i] is not None:
        #logging.debug(standings[i])
        #logging.debug(standings[i]['team']['code'])
        team = TeamStanding(standings[i]['team']['code'])
        team.name = standings[i]['team']['team']
        team.wins = standings[i]['team']['w']
        team.losses = standings[i]['team']['l']
        team.pct = standings[i]['team']['pct']
        team.gb = standings[i]['team']['gb']
        team.last10 = standings[i]['team']['last10']
        teams.append(team)

    return teams