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
import logging
import xml.dom.minidom


from google.appengine.api import urlfetch

class Game():
  def __init__ (self, game_id):
    self.game_id = game_id

class Team():
  def __init__ (self, id):
    self.id = id

class Stadium():
  def __init__ (self, id):
    self.id = id

'''
Fetch XML for the game id.
Sample URL:  http://gd2.mlb.com/components/game/mlb/year_2008/month_04/day_07/gid_2008_04_07_flomlb_wasmlb_1/game.xml
'''
def fetchGame(game_id):
  gid_pieces = game_id.split('_')
  logging.info(gid_pieces[0])
  logging.info(gid_pieces[1])
  logging.info(gid_pieces[2])
  url = "http://gd2.mlb.com/components/game/mlb/year_"+gid_pieces[0]+"/month_"+gid_pieces[1]+"/day_"+gid_pieces[2]+"/gid_"+game_id+"/game.xml"
  url = url.encode("utf-8")
  #logging.info(url)
  headers = { 'Host': 'gd2.mlb.com', 'Content-Type': 'text/xml', 'Accept': 'text/xml' }
  result = urlfetch.fetch(url, headers=headers)
  return xml.dom.minidom.parseString(result.content)

def buildGame(node, game_id):
  logging.info("inside buildGame")
  game = Game(game_id)
  game.type = node.getAttribute("type")
  game.local_game_time = node.getAttribute("local_game_time")
  game.gameday_sw = node.getAttribute("gameday_sw")
  for gcn in node.childNodes:
    if gcn.nodeType == node.ELEMENT_NODE:
      if gcn.tagName == "team":
        team = Team(gcn.getAttribute("id"))
        team.type = gcn.getAttribute("type")
        team.code = gcn.getAttribute("code")
        team.file_code = gcn.getAttribute("file_code")
        team.abbrev = gcn.getAttribute("abbrev")
        team.name = gcn.getAttribute("name")
        team.w = gcn.getAttribute("w")
        team.l = gcn.getAttribute("l")
        team.league = gcn.getAttribute("league")
        if team.type == "home":
          game.home_team = team
        else:
          game.away_team = team
      if gcn.tagName == "stadium":
        stadium = Stadium(gcn.getAttribute("id"))
        stadium.name = gcn.getAttribute("name")
        stadium.venue_w_chan_loc = gcn.getAttribute("venue_w_chan_loc")
        stadium.location = gcn.getAttribute("location")
        game.stadium = stadium
  return game