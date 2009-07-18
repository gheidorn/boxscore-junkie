#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    json_helper_game.py handles the fetch and parse of a JavaScript file from the MLB
#    
#    $Id: json_helper.py 10 2009-05-05 00:01:06Z greg.heidorn@gmail.com $
import logging
import xml.dom.minidom
import yaml

from django.utils import simplejson
from models import *
from google.appengine.api import urlfetch
'''
Fetch JSON data for the standings for the given day.
Divisions are ale, alc, alw, nle, nlc, nlw (e.g. National League West)
Sample URL:  http://mlb.mlb.com/components/game/year_2009/month_07/day_01/standings_rs_ale.js
'''
def fetchStandings(year, month, day, division):
  # massage parameters
  mm = str(month)
  dd = str(day)
  if month < 10:
    mm = "0" + str(month)
  if day < 10:
    dd = "0" + str(day)

  # build url
  url = "http://mlb.mlb.com/components/game/year_"+str(year)+"/month_"+mm+"/day_"+dd+"/standings_rs_"+division+".js"
  url = url.encode("utf-8")
  #logging.debug("fetchStandings for " + division + " on " + mm + " " + dd + " " + str(year))
  #logging.debug(url)

  # build http headers
  headers = { 'Host': 'mlb.mlb.com', 'Content-Type': 'text/javascript', 'Accept': 'text/javascript' }
  
  # fetch data
  result = urlfetch.fetch(url, headers=headers)

  # rip off javascript variable assignment
  json = result.content[23:]
  
  #y = yaml.load(json.replace('\n', '').replace('\t', '').replace('mode:', 'mode-').replace('lurl:','lurl'))
  
  #logging.debug(json)

  # ugly, ridiculous hack to repair broken json
  # 1 - change var name lurl in 'wrap' to prevent later replacement of 'l'        replace("lurl", "LURL")
  # 2 - remove { from 'wrap' to prevent later replacement of {                    replace('{gid', 'gid')
  # 3 - remove } from 'wrap' to prevent later replacement of }                    replace("\\\'}","")
  # 4 - remove /' from 'wrap' to prevent confusion of later replacement of '      replace("\\'","")
  # 5 - replace ' with " for values to follow JSON rules                          replace("'", '"')
  # 6 through 37 - replace key: pattern with "key": pattern to follow JSON rules  replace('w:', '"w":')
  # 38 - replace { with {"team":{ to create key-value pair to follow JSON rules   replace('{', '{"team":{')
  # 39 - replace } with }} to close off new key-value pair                        replace('}', '}}')
  x = json.replace('"', '').replace("lurl", "LURL").replace('{gid', 'gid').replace("\\\'}","").replace("\\'","").replace("'", '"').replace('w:', '"w":').replace('elim:', '"elim":').replace('rs:', '"rs":').replace('div:', '"div":').replace('gameid:', '"gameid":').replace('status:', '"status":').replace('pre:', '"pre":').replace('last10:', '"last10":').replace('onerun:', '"onerun":').replace('xtr:', '"xtr":').replace('nextg:', '"nextg":').replace('vsW:', '"vsW":').replace('ra:', '"ra":').replace('gb:', '"gb":').replace('wrap:', '"wrap":').replace('home:', '"home":').replace('code:', '"code":').replace('pct:', '"pct":').replace('league_sensitive_team_name:', '"league_sensitive_team_name":').replace('vsC:', '"vsC":').replace('vsE:', '"vsE":').replace('clinch:', '"clinch":').replace('vsR:', '"vsR":').replace('vsL:', '"vsL":').replace('xwl:', '"xwl":').replace('strk:', '"strk":').replace('l:', '"l":').replace('lastg:', '"lastg":').replace('interleague:', '"interleague":').replace('team:', '"team":').replace('road:', '"road":').replace('{', '{"team":{').replace('}', '}}')
  #logging.debug(x)
  
  standings = simplejson.loads(x)
    
  if "GameDay - 404 Not Found" in result.content:
    return None
  else:
    return standings