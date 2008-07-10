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

import xml_helper_players
from db_models import *

from datetime import datetime

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PutPlayerHandler(webapp.RequestHandler):
  def post(self):
    logging.info("start xml_helper_players")
    logging.info(datetime.today())
    #logging.info(self.request.get('gid'))
    game_id = self.request.get('gid')
    gameDOM = xml_helper_players.fetchPlayers(game_id)
    game = xml_helper_players.buildGame(gameDOM.getElementsByTagName("game")[0], game_id)
    logging.info(datetime.today())
    logging.info("end xml_helper_players")
    logging.info("start check/write")
    logging.info(datetime.today())
    action = "no write"
    writeCtr = 0
    for player in game.home_team.players:
      #logging.info(player.last)
      # check database for this team first
      q = DBPlayer.gql("WHERE id = :1", int(player.id))
      results = q.fetch(1)
      if results == []:
        if player.num == "":
          player.num = 0
        dbPlayer = DBPlayer(id=int(player.id),
                            team_id=game.home_team.id,
                            first=player.first,
                            last=player.last,
                            num=int(player.num),
                            boxname=player.boxname,
                            rl=player.rl,
                            position=player.position,
                            status=player.status)
        dbPlayer.put()
        action = "write"
        writeCtr += 1
    logging.info(datetime.today())
    logging.info("end check/write")
    
    if action == "write":
      action += " " + str(writeCtr)

    template_values = {
      'action': action,
      'players': getPlayers()
    }

    path = os.path.join(os.path.dirname(__file__), 'html/player.html')
    self.response.out.write(template.render(path, template_values))

  def get(self):

    action = "show form"

    template_values = {
      'action': action,
      'players': getPlayers()
    }

    path = os.path.join(os.path.dirname(__file__), 'html/player.html')
    self.response.out.write(template.render(path, template_values))

class GetTeamHandler(webapp.RequestHandler):
  def get(self):
    ctr = 0
    if self.request.get('arg') == "all":
      teams = getTeams()
      ctr = len(teams)
    else:
      team_id = self.request.get('arg')
      q = DBTeam.gql("WHERE id = :1", int(team_id))
      teams = q.fetch(5)
      
      for t in teams:
        ctr = ctr + 1

    template_values = {
      'action': "found " + str(ctr),
      'teams': teams
    }
    path = os.path.join(os.path.dirname(__file__), 'html/team.html')
    self.response.out.write(template.render(path, template_values))

class WipePlayersHandler(webapp.RequestHandler):
  def get(self):
    q = DBPlayer.all()
    results = q.fetch(1000)
    for r in results:
      r.delete()

    q = DBPlayer.all()
    results = q.fetch(5)

    action = "not wiped"
    if results == []:
      action = "wiped"

    template_values = {
      'action': action
    }
    path = os.path.join(os.path.dirname(__file__), 'html/player.html')
    self.response.out.write(template.render(path, template_values))

def getPlayers():
  logging.info("start getPlayers")
  logging.info(datetime.today())
  q = DBPlayer.all()
  q.order("last")
  results = q.fetch(1000)
  players = []
  for r in results:
    players.append(r)
  logging.info(datetime.today())
  logging.info("end getPlayers")
  return players

def getTeamsWithPlayers():
  logging.info("start getPlayers")
  logging.info(datetime.today())
  q = db.GqlQuery("select team_id from DBPlayer")
  results = q.fetch(30)
  logging.info(datetime.today())
  logging.info("end getPlayers")
  return results

def main():
  application = webapp.WSGIApplication([('/data/player/wipe', WipePlayersHandler),
                                        ('/data/player/put', PutPlayerHandler),
                                        ('/data/team/get', GetTeamHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()