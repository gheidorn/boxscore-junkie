#!/usr/bin/env python
#
# Copyright 2008 Greg Heidorn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import array
import cgi
import logging
import os
import wsgiref.handlers
import xml.dom.minidom

import xml_helper
import xml_helper_highlights

from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

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

    # build menu tabs
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)

    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]

    # build the day's GameDay object
    gameday = xml_helper.buildGameDay(gamesNode)
    gameday.yesterday_date = date(int(gameday.year), int(gameday.month), int(gameday.day)) - timedelta(days=1)

    # build an array of the day's games
    games = []
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        games.append(xml_helper.buildGame(node))

    template_values = {
      'gameday': gameday,
      'games': games,
      'lastUpdate': datetime.today(),
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/scoreboard-live.html')
    self.response.out.write(template.render(path, template_values))

class BoxscoreHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

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
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
        games.append(game)

    template_values = {
      'gid': gid,
      'gameday': gameday,
      'games': games,
      'game': selectedGame,
      'boxscore': boxscore,
      'lastUpdate': datetime.today(),
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/boxscore-live.html')
    self.response.out.write(template.render(path, template_values))

class PlayByPlayHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

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
      'lastUpdate': datetime.today(),
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/playbyplay-live.html')
    self.response.out.write(template.render(path, template_values))

class PitchByPitchHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh != "on":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

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
      'lastUpdate': datetime.today(),
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/pitchbypitch-live.html')
    self.response.out.write(template.render(path, template_values))

class HighlightsHandler(webapp.RequestHandler):
  def get(self):
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

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
      'lastUpdate': datetime.today(),
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay
    }

    path = os.path.join(os.path.dirname(__file__), 'html/highlights.html')
    self.response.out.write(template.render(path, template_values))

class BatterPBPHandler(webapp.RequestHandler):
  def get(self):
    bid = self.request.get('bid')
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    boxscore = {}
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
        games.append(game)
    
    pbpDOM = xml_helper.fetchBatterPBP(year, month, day, gid, bid)
    batterNode = pbpDOM.getElementsByTagName("player")[0]
    batterPBP = xml_helper.buildBatterPBP(batterNode)

    logging.info(batterPBP.atbats)

    template_values = {
      'gid': gid,
      'bid': bid,
      'gameday': gameday,
      'games': games,
      'boxscore': boxscore,
      'batterPBP': batterPBP,
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay
    }

    path = os.path.join(os.path.dirname(__file__), 'html/core.html')
    self.response.out.write(template.render(path, template_values))

class PitcherPBPHandler(webapp.RequestHandler):
  def get(self):
    pid = self.request.get('pid')
    gid = self.request.get('gid')
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    selDay = date(int(year), int(month), int(day))
    prevDay = selDay - timedelta(days=1)
    nextDay = selDay + timedelta(days=1)
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(year, month, day)
    gamesNode = masterScoreboardDOM.getElementsByTagName("games")[0]
    gameday = xml_helper.buildGameDay(gamesNode)

    games = []
    boxscore = {}
    for node in gamesNode.childNodes:
      if node.nodeType == node.ELEMENT_NODE:
        game = xml_helper.buildGame(node)
        if gid == game.gameday:
          boxscoreDOM = xml_helper.fetchBoxscore(gameday.year, gameday.month, gameday.day, game.gameday)
          boxscoreNode = boxscoreDOM.getElementsByTagName("boxscore")[0]
          boxscore = xml_helper.buildBoxscore(boxscoreNode)
        games.append(game)

    pbpDOM = xml_helper.fetchPitcherPBP(year, month, day, gid, pid)
    pitcherNode = pbpDOM.getElementsByTagName("player")[0]
    pitcherPBP = xml_helper.buildPitcherPBP(pitcherNode)

    template_values = {
      'gid': gid,
      'pid': pid,
      'gameday': gameday,
      'games': games,
      'boxscore': boxscore,
      'pitcherPBP': pitcherPBP,
      'prevDay': prevDay,
      'selDay': selDay,
      'nextDay': nextDay
    }

    path = os.path.join(os.path.dirname(__file__), 'html/core.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/scoreboard', MasterScoreboardHandler),
                                        ('/boxscore', BoxscoreHandler),
                                        ('/playbyplay', PlayByPlayHandler),
                                        ('/pitchbypitch', PitchByPitchHandler),
                                        ('/highlights', HighlightsHandler),
                                        ('/batterpbp', BatterPBPHandler),
                                        ('/pitcherpbp', PitcherPBPHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
