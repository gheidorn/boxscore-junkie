#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    main.py contains the request handlers for the site
#    
#    $Id$
import logging
import os
import wsgiref.handlers
import xml.dom.minidom

import standings_helper
import xml_helper
import xml_helper_highlights

from datetime import date
from datetime import datetime
from datetime import timedelta

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class Preferences(db.Model):
  user = db.UserProperty(db.Key)
  teamsToTrack = db.StringListProperty()

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
    
    # get user data
    user = users.get_current_user()
    teamsToTrack = ""
    if user is not None:
      userKeyName = "key:" + user.email()
      p = Preferences.get_by_key_name(userKeyName)
      if p is not None:
        teamsToTrack = p.teamsToTrack
    loginURL = users.create_login_url("/")
    logoutURL = users.create_logout_url("/")
    
    values = {
        'lastUpdate': lastUpdate.strftime("%m/%d %I:%M:%S %p"),
        'prevDay': prevDay,
        'today': today,
        'nextDay': nextDay,
        'r': refresh,
        't': refreshTime,
        'user': user,
        'teamsToTrack': teamsToTrack,
        'loginURL': loginURL,
        'logoutURL': logoutURL
    }
    
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('html', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class StandingsPage(BaseRequestHandler):
  def get(self):
    template = "standings.html"
    template_values = {  }
    self.generate(template, template_values)

class PreferencesPage(BaseRequestHandler):
  def get(self):
    template = "preferences.html"
    template_values = {  }
    self.generate(template, template_values)

class SavePreferences(BaseRequestHandler):
  def post(self):
    user = users.get_current_user()
    userKeyName = "key:" + user.email()
    prefs = Preferences(parent=None, key_name=userKeyName)
    prefs.user = user
    prefs.teamsToTrack = self.request.get_all("teamsToTrack");
    prefs.put()
    template = "preferences.html"
    template_values = { 'teamsToTrack': prefs.teamsToTrack, 'msg': 'saved' }
    self.generate(template, template_values)

class LiveScoreboardPage(BaseRequestHandler):
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

    # if user is logged in, retrieve preferences
    q = Preferences.gql("WHERE user = :1", users.get_current_user())
    results = q.fetch(1)
    
    teamsToTrack = []
    for p in results:
      teamsToTrack = p.teamsToTrack

    # get standings
    standings = standings_helper.getStandings(today.year, today.month, today.day)
    
    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(str(today.year), month, day)

    template_values = { 'selDay': today, 
                        'selDayStr': today.strftime("%B %d, %Y"),
                        'teamsToTrack': teamsToTrack,
                        'standings': standings }
    
    if masterScoreboardDOM is None:
      template = "no-games-today.html"
    else:
      gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]

      if gamesNode.childNodes.length == 0:
        template = "no-games-today.html"
      else:
        template = "scoreboard.html"

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

class PastScoreboardHandler(BaseRequestHandler):
  def get(self):
    # Process request data.
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    if len(month) == 1:
      month = "0" + month
    if len(day) == 1:
      day = "0" + day

    # build selected date
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)    

    # get standings
    standings = standings_helper.getStandings(selDay.year, selDay.month, selDay.day)

    template_values = {
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay,
      'selDayStr': selDay.strftime("%B %d, %Y"),
      'standings': standings
    }

    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    if masterScoreboardDOM is None:
      template = "no-games-today.html"
    else:
      gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]

      if gamesNode.childNodes.length == 0:
        template = "no-games-today.html"
      else:
        template = "scoreboard.html"

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

class BoxscoreHandler(BaseRequestHandler):
  def get(self):
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

    template = "boxscore.html"
    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay
    }

    self.generate(template, template_values)
    
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


def main():
  application = webapp.WSGIApplication([('/', LiveScoreboardPage),
                                        ('/scoreboard', PastScoreboardHandler),
                                        ('/preferences', PreferencesPage),
                                        ('/savePreferences', SavePreferences),
                                        ('/calendar', CalendarHandler),
                                        ('/cal', CalHandler),
                                        ('/boxscore', BoxscoreHandler),
                                        ('/playbyplay', PlayByPlayHandler),
                                        ('/pitchbypitch', PitchByPitchHandler),
                                        ('/highlights', HighlightsPage)], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()