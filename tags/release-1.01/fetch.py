#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    xml_helper_game.py handles the fetching of XML for AJAX clients
#    
#    $Id$
import cgi
import logging
import os
import wsgiref.handlers

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class FetchGamesHandler(webapp.RequestHandler):
  def get(self):
    year = self.request.get('year')
    month = self.request.get('month')
    day = self.request.get('day')
    
    if len(month) == 1:
      month = "0" + month
    
    if len(day) == 1:
      day = "0" + day

    url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/master_scoreboard.xml"
    url = url.encode("utf-8")
    
    logging.info(url)
    
    ''' not needed, but might investigate pros/cons of setting '''
    headers = { 
      'Content-Type': 'text/xml',
      'Accept': 'text/xml'
    }
    
    result = urlfetch.fetch(url, headers=headers)
    self.response.headers['Content-Type'] = 'text/xml'
    if result.status_code == 200:
      self.response.out.write(result.content)
    else:
      errorXml = "<errors><error>failed to fetch games for " + month + "/" + day + "/" + year + "</message></errors>"
      self.response.out.write(errorXml)

class FetchPlayersHandler(webapp.RequestHandler):
  def get(self):
    gameId = self.request.get('game')
    year = self.request.get('year')
    month = self.request.get('month')
    if len(month) == 1:
      month = "0" + month

    day = self.request.get('day')
    if len(day) == 1:
      day = "0" + day

    url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gameId+"/players.xml"
    url = url.encode("utf-8")
    logging.info(url)

    headers = { 
      'Content-Type': 'text/xml',
      'Accept': 'text/xml'
    }

    result = urlfetch.fetch(url, headers=headers)
    self.response.headers['Content-Type'] = 'text/xml'
    if result.status_code == 200:
      self.response.out.write(result.content)
    else:
      errorXml = "<errors>"
      errorXml += "<error message=\"failed to fetch players for " + month + "/" + day + "/" + year + "\"/>"
      errorXml += "</errors>"
      self.response.out.write(errorXml)

class FetchBoxscoreHandler(webapp.RequestHandler):
  def get(self):
    gameId = self.request.get('game')
    year = self.request.get('year')
    month = self.request.get('month')
    if len(month) == 1:
      month = "0" + month

    day = self.request.get('day')
    if len(day) == 1:
      day = "0" + day

    url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gameId+"/boxscore.xml"
    url = url.encode("utf-8")
    logging.info(url)

    ''' not needed, but might investigate pros/cons of setting '''
    headers = { 
      'Content-Type': 'text/xml',
      'Accept': 'text/xml'
    }

    result = urlfetch.fetch(url, headers=headers)
    self.response.headers['Content-Type'] = 'text/xml'
    if result.status_code == 200:
      self.response.out.write(result.content)
    else:
      errorXml = "<errors>"
      errorXml += "<error message=\"failed to fetch pitchers for " + month + "/" + day + "/" + year + "\"/>"
      errorXml += "</errors>"
      self.response.out.write(errorXml)

class FetchPBPBatterHandler(webapp.RequestHandler):
  def get(self):
    pid = self.request.get('pid')
    gid = self.request.get('game')
    year = self.request.get('year')
    month = self.request.get('month')
    if len(month) == 1:
      month = "0" + month
    day = self.request.get('day')
    if len(day) == 1:
      day = "0" + day

    url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gid+"/pbp/batters/"+pid+".xml"
    url = url.encode("utf-8")
    logging.info(url)

    ''' not needed, but might investigate pros/cons of setting '''
    headers = { 
      'Content-Type': 'text/xml',
      'Accept': 'text/xml'
    }

    result = urlfetch.fetch(url, headers=headers)
    self.response.headers['Content-Type'] = 'text/xml'
    if result.status_code == 200:
      self.response.out.write(result.content)
    else:
      errorXml = "<errors>"
      errorXml += "<error message=\"failed to fetch pitchers for " + month + "/" + day + "/" + year + "\"/>"
      errorXml += "</errors>"
      self.response.out.write(errorXml)

class FetchPBPPitcherHandler(webapp.RequestHandler):
  def get(self):
    pid = self.request.get('pid')
    gid = self.request.get('game')
    year = self.request.get('year')
    month = self.request.get('month')
    if len(month) == 1:
      month = "0" + month
    day = self.request.get('day')
    if len(day) == 1:
      day = "0" + day

    url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+gid+"/pbp/pitchers/"+pid+".xml"
    url = url.encode("utf-8")
    logging.info(url)

    ''' not needed, but might investigate pros/cons of setting '''
    headers = { 
      'Content-Type': 'text/xml',
      'Accept': 'text/xml'
    }

    result = urlfetch.fetch(url, headers=headers)
    self.response.headers['Content-Type'] = 'text/xml'
    if result.status_code == 200:
      self.response.out.write(result.content)
    else:
      errorXml = "<errors>"
      errorXml += "<error message=\"failed to fetch pitchers for " + month + "/" + day + "/" + year + "\"/>"
      errorXml += "</errors>"
      self.response.out.write(errorXml)

def main():
  application = webapp.WSGIApplication([('/fetch/games', FetchGamesHandler),
                                        ('/fetch/players', FetchPlayersHandler),
                                        ('/fetch/boxscore', FetchBoxscoreHandler),
                                        ('/fetch/pbp-batter', FetchPBPBatterHandler),
                                        ('/fetch/pbp-pitcher', FetchPBPPitcherHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
