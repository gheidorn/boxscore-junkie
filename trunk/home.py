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
import cgi
import logging
import os
import wsgiref.handlers
import xml.dom.minidom
import xml_helper
from datetime import date
from datetime import datetime
from datetime import timedelta
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class HomeHandler(webapp.RequestHandler):
  def get(self):
    refresh = self.request.get('r')
    if refresh == "":
      refresh = "off";
    refreshTime = self.request.get('t')
    if refreshTime == "":
      refreshTime = 60
    today = datetime.today() - timedelta(hours=5)
    #logging.info(datetime.today()- timedelta(hours=5))
    prevDay = today - timedelta(days=1)
    nextDay = today + timedelta(days=1)

    month = str(today.month)
    day = str(today.day)
    if today.month < 10:
      month = "0" + str(today.month)
    if today.day < 10:
      day = "0" + str(today.day)

    # retrieve xml for the day's scoreboard
    masterScoreboardDOM = xml_helper.fetchMasterScoreboard(str(today.year), month, day)
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
      'lastUpdate': datetime.today() - timedelta(hours=5),
      'prevDay': prevDay,
      'selDay': today,
      'nextDay': nextDay,
      'r': refresh,
      't': refreshTime
    }

    path = os.path.join(os.path.dirname(__file__), 'html/scoreboard-live.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', HomeHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
