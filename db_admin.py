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

import xml_helper_game
from db_models import *

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PutTeamHandler(webapp.RequestHandler):
  def post(self):
    logging.info(self.request.get('gid'))
    game_id = self.request.get('gid')
    gameDOM = xml_helper_game.fetchGame(game_id)
    game = xml_helper_game.buildGame(gameDOM.getElementsByTagName("game")[0], game_id)
    #logging.info("home team league: " + game.home_team.league)
    
    # check database for this team first
    q = DBTeam.gql("WHERE id = :1", int(game.home_team.id))
    results = q.fetch(1)
    logging.info("checking results")
    logging.info(results)
    
    team = {}
    for r in results:
      team = r
    
    action = "no write"

    if team == {}:
      homeTeam = DBTeam(id=int(game.home_team.id),
                        name=game.home_team.name,
                        code=game.home_team.code,
                        file_code=game.home_team.file_code,
                        abbrev=game.home_team.abbrev,
                        league=game.home_team.league)
      homeTeam.put()
      action = "write"
      team = homeTeam

    template_values = {
      'action': action,
      'teams': getTeams()
    }
    path = os.path.join(os.path.dirname(__file__), 'html/team.html')
    self.response.out.write(template.render(path, template_values))

  def get(self):
    logging.info(self.request.post('gid'))
    logging.info(self.request.get('gid'))
    game_id = self.request.get('gid')
    gameDOM = xml_helper_game.fetchGame(game_id)
    game = xml_helper_game.buildGame(gameDOM.getElementsByTagName("game")[0], game_id)
    #logging.info("home team league: " + game.home_team.league)
    
    # check database for this team first
    q = DBTeam.gql("WHERE id = :1", int(game.home_team.id))
    results = q.fetch(1)
    logging.info("checking results")
    logging.info(results)
    
    team = {}
    for r in results:
      logging.info("whee")
      team = r
    
    action = "no write"
    if team == {}:
      homeTeam = DBTeam(id=int(game.home_team.id),
                        name=game.home_team.name,
                        code=game.home_team.code,
                        file_code=game.home_team.file_code,
                        abbrev=game.home_team.abbrev,
                        league=game.home_team.league)
      homeTeam.put()
      action = "write"
      team = homeTeam

    template_values = {
      'action': action,
      'team': team
    }
    path = os.path.join(os.path.dirname(__file__), 'html/team.html')
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

class WipeTeamsHandler(webapp.RequestHandler):
  def get(self):
    q = db.GqlQuery("SELECT * FROM DBTeam")
    results = q.fetch(5)
    team = {}
    for r in results:
      r.delete()

    q = db.GqlQuery("SELECT * FROM DBTeam WHERE id = :1", 139)
    results = q.fetch(5)
    team = {}
    for r in results:
      team = r

    action = "not wiped"
    if team == {}:
      action = "wiped"

    template_values = {
      'action': action,
      'team': team
    }
    path = os.path.join(os.path.dirname(__file__), 'html/team.html')
    self.response.out.write(template.render(path, template_values))

def getTeams():
  q = DBTeam.all()
  q.order("name")
  results = q.fetch(30)
  teams = []
  for r in results:
    teams.append(r)
  return teams

def main():
  application = webapp.WSGIApplication([('/data/team/wipe', WipeTeamsHandler),
                                        ('/data/team/put', PutTeamHandler),
                                        ('/data/team/get', GetTeamHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()