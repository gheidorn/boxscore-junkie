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
Fetch XML DOM for the 'master scoreboard' for the given day.
Sample URL:  http://gd2.mlb.com/components/game/mlb/year_2008/month_05/day_19/gid_2008_05_19_chnmlb_houmlb_1/media/highlights.xml
'''
def fetchHighlights(year, month, day, gid):
  url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gid+"/media/highlights.xml"
  url = url.encode("utf-8")
  #logging.info(url)
  headers = { 'Host': 'gd2.mlb.com', 'Content-Type': 'text/xml', 'Accept': 'text/xml' }
  result = urlfetch.fetch(url, headers=headers)
  if "GameDay - 404 Not Found" in result.content:
    return None
  else:
    return xml.dom.minidom.parseString(result.content)

def buildHighlights(node, gid):
  highlights = Highlights(gid)
  highlights.medias = []
  for mediaNode in node.childNodes:
    if mediaNode.nodeType == node.ELEMENT_NODE:
      if mediaNode.tagName == "media":
        highlights.medias.append(buildMedia(mediaNode))
  return highlights

def buildMedia(node):
  media = Media(node.getAttribute("id"))
  media.type = node.getAttribute("type")
  media.date = node.getAttribute("date")
  media.v = node.getAttribute("v")
  media.keywords = []
  media.urls = []
  for childNode in node.childNodes:
    if childNode.nodeType == node.ELEMENT_NODE:
      if childNode.tagName == "headline":
        media.headline = childNode.firstChild.wholeText
      if childNode.tagName == "duration":
        media.duration = childNode.firstChild.wholeText
      if childNode.tagName == "keywords":
        for keywordNode in childNode.childNodes:
          if keywordNode.nodeType == node.ELEMENT_NODE:
            media.keywords.append(buildMediaKeyword(keywordNode))
      if childNode.tagName == "thumb":
        media.thumb = childNode.firstChild.wholeText
      if childNode.tagName == "url":
        media.urls.append(buildMediaUrl(childNode))
  return media

def buildMediaUrl(node):
  mediaUrl = MediaUrl(node.getAttribute("id"))
  mediaUrl.playback_scenario = node.getAttribute("playback_scenario")
  mediaUrl.authorization = node.getAttribute("authorization")
  mediaUrl.login = node.getAttribute("login")
  mediaUrl.mid = node.getAttribute("mid")
  mediaUrl.cat_code = node.getAttribute("cat_code")
  mediaUrl.state = node.getAttribute("state")
  mediaUrl.url = node.firstChild.wholeText
  return mediaUrl

def buildMediaKeyword(node):
  mediaKeyword = MediaKeyword(node.getAttribute("type"))
  mediaKeyword.value = node.getAttribute("value")
  return mediaKeyword