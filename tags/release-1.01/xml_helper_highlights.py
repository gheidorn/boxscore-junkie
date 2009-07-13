#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    xml_helper_game.py handles the fetch and parse of XML from the MLB datasource
#    
#    $Id$
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