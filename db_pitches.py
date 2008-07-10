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
from models import *
from google.appengine.api import urlfetch

'''
Fetch XML DOM for the 'pitch-by-pitch' for the givenday, game id & pitcher.
Sample URL:  http://gd2.mlb.com/components/game/mlb/year_2008/month_04/day_07/gid_2008_04_07_atlmlb_colmlb_1/pbp/pitchers/114849.xml
'''
def fetchBatterPBP(year, month, day, gid, pid):
  url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gid+"/pbp/batters/"+pid+".xml"
  url = url.encode("utf-8")
  #logging.info(url)
  headers = { 'Host': 'gd2.mlb.com', 'Content-Type': 'text/xml', 'Accept': 'text/xml' }
  result = urlfetch.fetch(url, headers=headers)
  return xml.dom.minidom.parseString(result.content)

'''
Fetch XML DOM for the 'pitch-by-pitch' for the givenday, game id & batter.
Sample URL:  http://gd2.mlb.com/components/game/mlb/year_2008/month_04/day_07/gid_2008_04_07_atlmlb_colmlb_1/pbp/batters/114849.xml
'''
def fetchPitcherPBP(year, month, day, gid, pid):
  url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gid+"/pbp/pitchers/"+pid+".xml"
  url = url.encode("utf-8")
  #logging.info(url)
  headers = { 'Host': 'gd2.mlb.com', 'Content-Type': 'text/xml', 'Accept': 'text/xml' }
  result = urlfetch.fetch(url, headers=headers)
  return xml.dom.minidom.parseString(result.content)

'''
Add pitches to the datasource.
'''
def buildPitcherPBP(node):
  pitcher = PitcherPBP(node.getAttribute("id"))
  pitcher.atbats = []
  for atbatNode in node.childNodes:
    if atbatNode.nodeType == node.ELEMENT_NODE:
      atbat = AtBat(atbatNode.getAttribute("num"))
      atbat.inning = atbatNode.getAttribute("inning")
      atbat.b = atbatNode.getAttribute("b")
      atbat.s = atbatNode.getAttribute("s")
      atbat.o = atbatNode.getAttribute("o")
      atbat.batter = atbatNode.getAttribute("batter")
      atbat.pitcher = atbatNode.getAttribute("pitcher")
      atbat.stand = atbatNode.getAttribute("stand")
      atbat.des = atbatNode.getAttribute("des")
      atbat.event = atbatNode.getAttribute("event")
      atbat.brief_event = atbatNode.getAttribute("brief_event")
      pitches = []
      for pitchNode in atbatNode.childNodes:
        if pitchNode.nodeType == node.ELEMENT_NODE:
          pitches.append(buildPitch(pitchNode))
      atbat.pitches = pitches
      pitcher.atbats.append(atbat)
  return pitcher

'''
Add pitches to the datasource.
'''
def buildBatterPBP(node):
  batter = BatterPBP(node.getAttribute("id"))
  batter.atbats = []
  for atbatNode in node.childNodes:
    if atbatNode.nodeType == node.ELEMENT_NODE:
      atbat = AtBat(atbatNode.getAttribute("num"))
      atbat.inning = atbatNode.getAttribute("inning")
      atbat.b = atbatNode.getAttribute("b")
      atbat.s = atbatNode.getAttribute("s")
      atbat.o = atbatNode.getAttribute("o")
      atbat.batter = atbatNode.getAttribute("batter")
      atbat.pitcher = atbatNode.getAttribute("pitcher")
      atbat.stand = atbatNode.getAttribute("stand")
      atbat.des = atbatNode.getAttribute("des")
      atbat.event = atbatNode.getAttribute("event")
      atbat.brief_event = atbatNode.getAttribute("brief_event")
      pitches = []
      for pitchNode in atbatNode.childNodes:
        if pitchNode.nodeType == node.ELEMENT_NODE:
          if pitchNode.tagName == "pitch":
            pitches.append(buildPitch(pitchNode))
      atbat.pitches = pitches
      batter.atbats.append(atbat)
  return batter

def buildPitch(node):
  pitch = Pitch(node.getAttribute("id"))
  pitch.des = node.getAttribute("des")
  pitch.type = node.getAttribute("type")
  pitch.x = node.getAttribute("x")
  pitch.y = node.getAttribute("y")
  if node.getAttribute("des") is not None:
    pitch.sv_id = node.getAttribute("sv_id")
    pitch.start_speed = node.getAttribute("start_speed")
    pitch.end_speed = node.getAttribute("end_speed")
    pitch.sz_top = node.getAttribute("sz_top")
    pitch.sz_bot = node.getAttribute("sz_bot")
    pitch.pfx_x = node.getAttribute("pfx_x")
    pitch.pfx_z = node.getAttribute("pfx_z")
    pitch.px = node.getAttribute("px")
    pitch.pz = node.getAttribute("pz")
    pitch.x0 = node.getAttribute("x0")
    pitch.y0 = node.getAttribute("y0")
    pitch.z0 = node.getAttribute("z0")
    pitch.vx0 = node.getAttribute("vx0")
    pitch.vy0 = node.getAttribute("vy0")
    pitch.vz0 = node.getAttribute("vz0")
    pitch.ax = node.getAttribute("ax")
    pitch.ay = node.getAttribute("ay")
    pitch.az = node.getAttribute("az")
    pitch.break_y = node.getAttribute("break_y")
    pitch.break_angle = node.getAttribute("break_angle")
    pitch.break_length = node.getAttribute("break_length")
    pitch.pitch_type = node.getAttribute("pitch_type")
    pitch.type_confidence = node.getAttribute("type_confidence")
  return pitch