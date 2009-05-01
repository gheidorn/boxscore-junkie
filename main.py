import logging
import os
import wsgiref.handlers
import xml.dom.minidom

import xml_helper
import xml_helper_highlights

from datetime import date
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    
    # handle refresh rate
    refresh = self.request.get('r')
    if refresh == "":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    
    # calculate dates
    today = datetime.today() - timedelta(hours=5)
    prevDay = today - timedelta(days=1)
    nextDay = today + timedelta(days=1)
    lastUpdate = datetime.today() - timedelta(hours=5)
    
    values = {
        'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
        'prevDay': prevDay,
        'today': today,
        'nextDay': nextDay,
        'r': refresh,
        't': refreshTime
    }
    
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('html', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class ScoreboardPage(BaseRequestHandler):
  """ displays current day's MLB scoreboard """
  def get(self):
    # manipulate current date to supply to XML fetch 
    today = datetime.today() - timedelta(hours=5)
    month = str(today.month)
    day = str(today.day)
    if today.month < 10:
      month = "0" + str(today.month)
    if today.day < 10:
      day = "0" + str(today.day)

    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(str(today.year), month, day)

    template_values = { 'selDay': today, 'selDayStr': today.strftime("%B %d, %Y") }
    
    if masterScoreboardDOM is None:
      template = "no-games-today.html"
    else:
      template = "scoreboard.html"
      gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]

      # build the day's GameDay object
      gameday = xml_helper.buildGameDay(gamesNode)
      gameday.yesterday_date = date(int(gameday.year), int(gameday.month), int(gameday.day)) - timedelta(days=1)

      # build an array of the day's games
      games = []
      for node in gamesNode.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
          games.append(xml_helper.buildGame(node))

      template_values['gameday'] = gameday
      template_values['games'] = games

    self.generate(template, template_values)

class CalendarHandler(webapp.RequestHandler):
  def get(self):
    year = self.request.get('y')
    
    if year == "":
      year = datetime.today().year 
    
    today = datetime.today() - timedelta(hours=6)
    prevDay = today - timedelta(days=1)
    nextDay = today + timedelta(days=1)

    yearList = ["2009", "2008", "2007"]

    template_values = {
      'prevDay': prevDay,
      'selDay': today,
      'today': today,
      'nextDay': nextDay,
      'year' : year,
      'yearList' : yearList
    }

    path = os.path.join(os.path.dirname(__file__), 'html/calendar.html')
    self.response.out.write(template.render(path, template_values))

class MasterScoreboardHandler(webapp.RequestHandler):
  def get(self):
    # Process request data.
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    if len(month) == 1:
      month = "0" + month
    if len(day) == 1:
      day = "0" + day

    lastUpdate = datetime.today() - timedelta(hours=5)

    # build dates
    today = datetime.today() - timedelta(hours=5)
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)

    template_values = {
      'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
      'prevDay': prevDay,
      'selDay': selDay,
      'selDayStr': today.strftime("%B %d, %Y"),
      'today': today,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    if masterScoreboardDOM is None:
      destination = "html/no-games-today.html"
    else:
      destination = "html/scoreboard.html"
      gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]

      # build the day's GameDay object
      gameday = xml_helper.buildGameDay(gamesNode)
      gameday.yesterday_date = date(int(gameday.year), int(gameday.month), int(gameday.day)) - timedelta(days=1)

      # build an array of the day's games
      games = []
      for node in gamesNode.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
          games.append(xml_helper.buildGame(node))

      template_values['gameday'] = gameday
      template_values['games'] = games

    path = os.path.join(os.path.dirname(__file__), destination)
    self.response.out.write(template.render(path, template_values))

class BoxscoreHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    
    ''' game id '''
    gid = self.request.get('gid')
    
    ''' derive year/month/day from the game id '''
    year = gid[:4]
    month = gid[5:7]
    day = gid[8:10]
    
    ''' determine dates for links based on date selected '''
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)    
    today = datetime.today() - timedelta(hours=5)
    lastUpdate = datetime.today() - timedelta(hours=5)
    
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    game = {}
    boxscore = {}
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          selectedGame = xml_helper.buildGame(node)
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          if boxscoreDOM is None:
            boxscore = {}
          else:
            boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
            boxscore = xml_helper.buildBoxscore(boxscoreNode)
        games.append(game)

    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
      'prevDay': prevDay,
      'selDay': selDay,
      'today': today,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/boxscore.html')
    self.response.out.write(template.render(path, template_values))

class PlayByPlayHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60

    ''' game id '''
    gid = self.request.get('gid')
    
    ''' derive year/month/day from the game id '''
    year = gid[:4]
    month = gid[5:7]
    day = gid[8:10]
    
    ''' determine dates for links based on date selected '''
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)    
    today = datetime.today() - timedelta(hours=5)
    lastUpdate = datetime.today() - timedelta(hours=5)
    
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    game = {}
    boxscore = {}
    innings = []
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          selectedGame = xml_helper.buildGame(node)
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
          for inning in range(int(game.game_status.inning)):
            inningDOM = xml_helper.fetchInning(gameday.year, gameday.month, gameday.day, game.gameday, inning+1)
            inningNode = inningDOM.getElementsByTagName("inning")[0]
            innings.append(xml_helper.buildInning(inningNode))
        games.append(game)

    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'innings': innings,
      'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
      'prevDay': prevDay,
      'selDay': selDay,
      'today': today,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/playbyplay.html')
    self.response.out.write(template.render(path, template_values))

class PitchByPitchHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60

    ''' game id '''
    gid = self.request.get('gid')
    
    ''' derive year/month/day from the game id '''
    year = gid[:4]
    month = gid[5:7]
    day = gid[8:10]
    
    ''' determine dates for links based on date selected '''
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)    
    today = datetime.today() - timedelta(hours=5)
    lastUpdate = datetime.today() - timedelta(hours=5)

    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    game = {}
    boxscore = {}
    innings = []
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          selectedGame = xml_helper.buildGame(node)
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
          for inning in range(int(game.game_status.inning)):
            inningDOM = xml_helper.fetchInning(gameday.year, gameday.month, gameday.day, game.gameday, inning+1)
            inningNode = inningDOM.getElementsByTagName("inning")[0]
            innings.append(xml_helper.buildInning(inningNode))
        games.append(game)

    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'innings': innings,
      'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
      'prevDay': prevDay,
      'selDay': selDay,
      'today': today,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/pitchbypitch.html')
    self.response.out.write(template.render(path, template_values))

class HighlightsPage(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60

    ''' game id '''
    gid = self.request.get('gid')
    
    ''' derive year/month/day from the game id '''
    year = gid[:4]
    month = gid[5:7]
    day = gid[8:10]
    
    ''' determine dates for links based on date selected '''
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)    
    today = datetime.today() - timedelta(hours=5)
    lastUpdate = datetime.today() - timedelta(hours=5)

    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    game = {}
    boxscore = {}
    highlights = {}
    innings = []
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          #selectedGame = xml_helper.buildGame(node)
          selectedGame = game
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
          highlightsDOM = xml_helper_highlights.fetchHighlights(gameday.year, gameday.month, gameday.day, game.gameday)
          if highlightsDOM is not None:
            highlightsNode = highlightsDOM.getElementsByTagName("highlights")[0]
            highlights = xml_helper_highlights.buildHighlights(highlightsNode, gid)
        games.append(game)

    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'highlights': highlights,
      'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
      'prevDay': prevDay,
      'selDay': selDay,
      'today': today,
      'nextDay': nextDay
    }

    path = os.path.join(os.path.dirname(__file__), 'html/highlights.html')
    self.response.out.write(template.render(path, template_values))


class CalHandler(webapp.RequestHandler):
  def get(self):
    year = self.request.get('y')
    
    if year == "":
      year = datetime.today().year 
    
    today = datetime.today() - timedelta(hours=6)
    prevDay = today - timedelta(days=1)
    nextDay = today + timedelta(days=1)

    yearList = ["2009", "2008", "2007"]

    template_values = {
      'prevDay': prevDay,
      'selDay': today,
      'today': today,
      'nextDay': nextDay,
      'year' : year,
      'yearList' : yearList
    }

    path = os.path.join(os.path.dirname(__file__), 'html/calendar2009.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', ScoreboardPage),
                                        ('/calendar', CalendarHandler),
                                        ('/cal', CalHandler),
                                        ('/scoreboard', MasterScoreboardHandler),
                                        ('/boxscore', BoxscoreHandler),
                                        ('/playbyplay', PlayByPlayHandler),
                                        ('/pitchbypitch', PitchByPitchHandler),
                                        ('/highlights', HighlightsPage)], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()