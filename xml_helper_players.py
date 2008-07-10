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

class Player():
  def __init__ (self, id):
    self.id = id

'''
Fetch XML for the game id.
Sample URL:  http://gd2.mlb.com/components/game/mlb/year_2008/month_04/day_07/gid_2008_04_07_flomlb_wasmlb_1/game.xml
'''
def fetchPlayers(game_id):
  gid_pieces = game_id.split('_')
  url = "http://gd2.mlb.com/components/game/mlb/year_"+gid_pieces[0]+"/month_"+gid_pieces[1]+"/day_"+gid_pieces[2]+"/gid_"+game_id+"/players.xml"
  url = url.encode("utf-8")
  headers = { 'Host': 'gd2.mlb.com', 'Content-Type': 'text/xml', 'Accept': 'text/xml' }
  result = urlfetch.fetch(url, headers=headers)
  return xml.dom.minidom.parseString(result.content)

def buildGame(node, game_id):
  game = Game(game_id)
  game.venue = node.getAttribute("venue")
  game.date = node.getAttribute("date")
  for gcn in node.childNodes:
    if gcn.nodeType == node.ELEMENT_NODE:
      if gcn.tagName == "team":
        team = Team(gcn.getAttribute("id"))
        team.type = gcn.getAttribute("type")
        team.name = gcn.getAttribute("name")
        team.players = []
        for teamNode in gcn.childNodes:
          if teamNode.nodeType == node.ELEMENT_NODE:
            if teamNode.tagName == "player":
              player = Player(teamNode.getAttribute("id"))
              player.team_id = team.id
              player.first = teamNode.getAttribute("first")
              player.last = teamNode.getAttribute("last")
              player.num = teamNode.getAttribute("num")
              player.boxname = teamNode.getAttribute("boxname")
              player.rl = teamNode.getAttribute("rl")
              player.position = teamNode.getAttribute("position")
              player.status = teamNode.getAttribute("status")
              team.players.append(player)
        if team.type == "home":
          game.home_team = team
        else:
          game.away_team = team
  return game