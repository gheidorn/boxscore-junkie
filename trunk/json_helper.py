#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    xml_helper_game.py handles the fetch and parse of XML from the MLB datasource
#    
#    $Id: xml_helper.py 10 2009-05-05 00:01:06Z greg.heidorn@gmail.com $
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
  logging.debug("fetchStandings for " + division + " on " + mm + " " + dd + " " + str(year))
  logging.debug(url)

  # build http headers
  headers = { 'Host': 'mlb.mlb.com', 'Content-Type': 'text/javascript', 'Accept': 'text/javascript' }
  
  # fetch data
  result = urlfetch.fetch(url, headers=headers)
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




'''
Build a GameDay object from the root node of the master_scoreboard.xml.
'''
def buildGameDay(node):
  gameday = GameDay(node.getAttribute("day"), node.getAttribute("month"), node.getAttribute("year"))
  gameday.modified_date = node.getAttribute("modified_date")
  gameday.next_day_date = node.getAttribute("next_day_date")
  return gameday

'''
Build a Game object from the <game> nodes of the master_scoreboard.xml.

If status/indicator is "Preview/S", then expect:
  home_probable_pitcher
  away_probable_pitcher
  links
  alerts? (yet to be seen)

If status/indicator is "Pre-Game/", then expect:

'''
def buildGame(node):
  game = Game(node.getAttribute("id"))
  game.ampm = node.getAttribute("ampm")
  game.venue = node.getAttribute("venue")
  game.game_pk = node.getAttribute("game_pk")
  game.time = node.getAttribute("time")
  game.time_zone = node.getAttribute("time_zone")
  game.game_type = node.getAttribute("game_type")
  game.away_name_abbrev = node.getAttribute("away_name_abbrev")
  game.home_name_abbrev = node.getAttribute("home_name_abbrev")
  game.away_code = node.getAttribute("away_code")
  game.away_file_code = node.getAttribute("away_file_code")
  game.away_team_id = node.getAttribute("away_team_id")
  game.away_team_city = node.getAttribute("away_team_city")
  game.away_team_name = node.getAttribute("away_team_name")
  game.away_division = node.getAttribute("away_division")
  game.home_code = node.getAttribute("home_code")
  game.home_file_code = node.getAttribute("home_file_code")
  game.home_team_id = node.getAttribute("home_team_id")
  game.home_team_city = node.getAttribute("home_team_city")
  game.home_team_name = node.getAttribute("home_team_name")
  game.home_division = node.getAttribute("home_division")
  game.day = node.getAttribute("day")
  game.gameday_sw = node.getAttribute("gameday_sw")
  game.away_games_back = node.getAttribute("away_games_back")
  game.home_games_back = node.getAttribute("home_games_back")
  game.away_games_back = node.getAttribute("away_games_back")
  game.home_games_back_wildcard = node.getAttribute("home_games_back_wildcard")
  game.venue_w_chan_loc = node.getAttribute("venue_w_chan_loc")
  game.gameday = node.getAttribute("gameday")
  game.away_win = node.getAttribute("away_win")
  game.away_loss = node.getAttribute("away_loss")
  game.home_win = node.getAttribute("home_win")
  game.home_loss = node.getAttribute("home_loss")
  game.league = node.getAttribute("league")
  for gameChildNode in node.childNodes:
    if gameChildNode.nodeType == node.ELEMENT_NODE:
      if gameChildNode.tagName == "status":
        game.game_status = buildGameStatus(gameChildNode)
      if gameChildNode.tagName == "home_probable_pitcher":
        game.home_probable_pitcher = buildGameProbablePitcher(gameChildNode)
      if gameChildNode.tagName == "away_probable_pitcher":
        game.away_probable_pitcher = buildGameProbablePitcher(gameChildNode)
      if gameChildNode.tagName == "linescore":
        game.linescore = buildGameLinescore(gameChildNode)
      if gameChildNode.tagName == "batter":
        game.batter = buildGameBatter(gameChildNode)
      if gameChildNode.tagName == "pitcher":
        game.pitcher = buildGamePitcher(gameChildNode)
      if gameChildNode.tagName == "opposing_pitcher":
        game.opposing_pitcher = buildGameOpposingPitcher(gameChildNode)
      if gameChildNode.tagName == "pbp":
        game.pbp = buildGamePBP(gameChildNode)
      if gameChildNode.tagName == "ondeck":
        game.ondeck = buildGameOnDeck(gameChildNode)
      if gameChildNode.tagName == "inhole":
        game.inhole = buildGameInHole(gameChildNode)
      if gameChildNode.tagName == "runners_on_base":
        game.runners_on_base = buildGameRunnersOnBase(gameChildNode)
      if gameChildNode.tagName == "links":
        game.links = buildGameLinks(gameChildNode)
      if gameChildNode.tagName == "alerts":
        game.alerts = buildGameAlerts(gameChildNode)
      if gameChildNode.tagName == "winning_pitcher":
        game.winning_pitcher = buildGameWinningPitcher(gameChildNode)
      if gameChildNode.tagName == "losing_pitcher":
        game.losing_pitcher = buildGameLosingPitcher(gameChildNode)
      if gameChildNode.tagName == "save_pitcher":
        game.save_pitcher = buildGameSavePitcher(gameChildNode)
      if gameChildNode.tagName == "home_runs":
        game.home_runs = buildGameHomeRuns(gameChildNode)
  return game

def buildGameStatus(node):
  gameStatus = GameStatus(node.getAttribute("status"))
  gameStatus.ind = node.getAttribute("ind")
  if(gameStatus.ind != "S"):
    gameStatus.reason = node.getAttribute("reason")
    gameStatus.inning = node.getAttribute("inning")
    gameStatus.top_inning = node.getAttribute("top_inning")
    gameStatus.b = node.getAttribute("b")
    gameStatus.s = node.getAttribute("s")
    gameStatus.o = node.getAttribute("o")
  return gameStatus

def buildGameProbablePitcher(node):
  probablePitcher = GameProbablePitcher(node.getAttribute("id"))
  probablePitcher.last = node.getAttribute("last")
  probablePitcher.first = node.getAttribute("first")
  probablePitcher.number = node.getAttribute("number")
  probablePitcher.wins = node.getAttribute("wins")
  probablePitcher.losses = node.getAttribute("losses")
  probablePitcher.era = node.getAttribute("era")
  return probablePitcher

'''
Need to check the order of Linescore Innings after XML parsing
'''
def buildGameLinescore(node):
  ls = GameLinescore()
  inningCtr = 1
  for lsChildNode in node.childNodes:
    if lsChildNode.nodeType == node.ELEMENT_NODE:
      if lsChildNode.tagName == "inning":
        inning = GameLinescoreInning(inningCtr)
        inning.home = lsChildNode.getAttribute("home")
        inning.away = lsChildNode.getAttribute("away")
        ls.innings.append(inning)
        inningCtr = inningCtr + 1
      if lsChildNode.tagName == "r":
        r = GameLinescoreRuns()
        r.away = lsChildNode.getAttribute("away")
        r.home = lsChildNode.getAttribute("home")
        r.diff = lsChildNode.getAttribute("diff")
        ls.r = r
      if lsChildNode.tagName == "h":
        h = GameLinescoreHits()
        h.away = lsChildNode.getAttribute("away")
        h.home = lsChildNode.getAttribute("home")
        ls.h = h
      if lsChildNode.tagName == "e":
        e = GameLinescoreErrors()
        e.away = lsChildNode.getAttribute("away")
        e.home = lsChildNode.getAttribute("home")
        ls.e = e
  return ls

'''
Build object from <batter> node in <game>.
'''
def buildGameBatter(node):
  batter = GameBatter(node.getAttribute("id"))
  batter.ab = node.getAttribute("ab")
  batter.h = node.getAttribute("h")
  batter.last = node.getAttribute("last")
  batter.first = node.getAttribute("first")
  batter.number = node.getAttribute("number")
  batter.avg = node.getAttribute("avg")
  batter.hr = node.getAttribute("hr")
  batter.rbi = node.getAttribute("rbi")
  return batter

'''
Build object from <pitcher> node in <game>.
'''
def buildGamePitcher(node):
  pitcher = GamePitcher(node.getAttribute("id"))
  pitcher.ip = node.getAttribute("ip")
  pitcher.er = node.getAttribute("er")
  pitcher.era = node.getAttribute("era")
  pitcher.wins = node.getAttribute("wins")
  pitcher.losses = node.getAttribute("losses")
  pitcher.last = node.getAttribute("last")
  pitcher.first = node.getAttribute("first")
  pitcher.number = node.getAttribute("number")
  return pitcher

'''
Build object from <opposing_pitcher> node in <game>.
'''
def buildGameOpposingPitcher(node):
  opp = GameOpposingPitcher(node.getAttribute("id"))
  opp.era = node.getAttribute("era")
  opp.wins = node.getAttribute("wins")
  opp.losses = node.getAttribute("losses")
  opp.last = node.getAttribute("last")
  opp.first = node.getAttribute("first")
  opp.number = node.getAttribute("number")
  return opp

'''
Build object from <pbp> node in <game>.
'''
def buildGamePBP(node):
  return GamePBP(node.getAttribute("last"))

'''
Build object from <on_deck> node in <game>.
'''
def buildGameOnDeck(node):
  ondeck = GameOnDeck(node.getAttribute("id"))
  ondeck.last = node.getAttribute("last")
  ondeck.first = node.getAttribute("first")
  ondeck.number = node.getAttribute("number")
  ondeck.avg = node.getAttribute("avg")
  ondeck.hr = node.getAttribute("hr")
  ondeck.rbi = node.getAttribute("rbi")
  return ondeck

'''
Build object from <in_hole> node in <game>.
'''
def buildGameInHole(node):
  inhole = GameInHole(node.getAttribute("id"))
  inhole.last = node.getAttribute("last")
  inhole.first = node.getAttribute("first")
  inhole.number = node.getAttribute("number")
  inhole.avg = node.getAttribute("avg")
  inhole.hr = node.getAttribute("hr")
  inhole.rbi = node.getAttribute("rbi")
  return inhole

'''
'''
def buildGameHomeRuns(node):
  hrs = GameHomeRuns()
  for hrNode in node.childNodes:
    if hrNode.nodeType == node.ELEMENT_NODE:
      hr = GameHomeRun(hrNode.getAttribute("id"))
      hr.last = hrNode.getAttribute("last")
      hr.first = hrNode.getAttribute("first")
      hr.number = hrNode.getAttribute("number")
      hr.hr = hrNode.getAttribute("hr")
      hr.std_hr = hrNode.getAttribute("std_hr")
      hr.inning = hrNode.getAttribute("inning")
      hr.runners = hrNode.getAttribute("runners")
      hr.team_code = hrNode.getAttribute("team_code")
      hrs.homeruns.append(hr)
  return hrs

'''
Build an object from <runners_on_base>.
'''
def buildGameRunnersOnBase(node):
  rob = GameRunnersOnBase(node.getAttribute("status"))
  for robChildNode in node.childNodes:
    if robChildNode.nodeType == node.ELEMENT_NODE:
      runner = GameRunnerOnBase(robChildNode.getAttribute("id"))
      runner.first = robChildNode.getAttribute("first")
      runner.last = robChildNode.getAttribute("last")
      runner.number = robChildNode.getAttribute("number")
      if robChildNode.tagName == "runner_on_1b":
        rob.runner_on_1b = runner
      if robChildNode.tagName == "runner_on_2b":
        rob.runner_on_2b = runner
      if robChildNode.tagName == "runner_on_3b":
        rob.runner_on_3b = runner
  return rob

'''
Build an object from <links>.
'''
def buildGameLinks(node):
  links = GameLinks(node.getAttribute("tv_station"))
  links.mlbtv = node.getAttribute("mlbtv")
  links.wrapup = node.getAttribute("wrapup")
  links.home_audio = node.getAttribute("home_audio")
  links.away_audio = node.getAttribute("away_audio")
  links.home_preview = node.getAttribute("home_preview")
  links.away_preview = node.getAttribute("away_preview")
  links.preview = node.getAttribute("preview")
  return links

'''
Build an object from <alerts>.
'''
def buildGameAlerts(node):
  alerts = GameAlerts(node.getAttribute("type"))
  alerts.text = node.getAttribute("text")
  alerts.brief_text = node.getAttribute("brief_text")
  return alerts
'''
Build object from <winning_pitcher> node in <game>.
'''
def buildGameWinningPitcher(node):
  pitcher = GamePitcher(node.getAttribute("id"))
  pitcher.era = node.getAttribute("era")
  pitcher.wins = node.getAttribute("wins")
  pitcher.losses = node.getAttribute("losses")
  pitcher.last = node.getAttribute("last")
  pitcher.first = node.getAttribute("first")
  pitcher.number = node.getAttribute("number")
  return pitcher
  
'''
Build object from <losing_pitcher> node in <game>.
'''
def buildGameLosingPitcher(node):
  pitcher = GamePitcher(node.getAttribute("id"))
  pitcher.era = node.getAttribute("era")
  pitcher.wins = node.getAttribute("wins")
  pitcher.losses = node.getAttribute("losses")
  pitcher.last = node.getAttribute("last")
  pitcher.first = node.getAttribute("first")
  pitcher.number = node.getAttribute("number")
  return pitcher

'''
Build object from <save_pitcher> node in <game>.
'''
def buildGameSavePitcher(node):
  pitcher = GamePitcher(node.getAttribute("id"))
  pitcher.era = node.getAttribute("era")
  pitcher.wins = node.getAttribute("wins")
  pitcher.losses = node.getAttribute("losses")
  pitcher.saves = node.getAttribute("saves")
  pitcher.last = node.getAttribute("last")
  pitcher.first = node.getAttribute("first")
  pitcher.number = node.getAttribute("number")
  return pitcher

'''
Build an object from <boxscore>.
'''
def buildBoxscore(node):
  boxscore = Boxscore(node.getAttribute("game_id"))
  boxscore.game_pk = node.getAttribute("game_pk")
  boxscore.home_sport_code = node.getAttribute("home_sport_code")
  boxscore.away_team_code = node.getAttribute("away_team_code")
  boxscore.home_team_code = node.getAttribute("home_team_code")
  boxscore.away_id = node.getAttribute("away_id")
  boxscore.home_id = node.getAttribute("home_id")
  boxscore.away_fname = node.getAttribute("away_fname")
  boxscore.home_fname = node.getAttribute("home_fname")
  boxscore.away_sname = node.getAttribute("away_sname")
  boxscore.home_sname = node.getAttribute("home_sname")
  boxscore.date = node.getAttribute("date")
  boxscore.away_wins = node.getAttribute("away_wins")
  boxscore.away_loss = node.getAttribute("away_loss")
  boxscore.home_wins = node.getAttribute("home_wins")
  boxscore.home_loss = node.getAttribute("home_loss")
  boxscore.status_ind = node.getAttribute("status_ind")
  
  boxscore.away_batters = []
  boxscore.away_pitchers = []
  boxscore.home_batters = []
  boxscore.home_pitchers = []
  boxscore.home_batter_notes = []
  boxscore.away_batter_notes = []
  for boxscoreChild in node.childNodes:
    if boxscoreChild.nodeType == node.ELEMENT_NODE:
      if boxscoreChild.tagName == "batting":
        teamAbbr = ""
        teamFlag = boxscoreChild.getAttribute("team_flag")
        '''
        if teamFlag == "home":
          teamAbbr = boxscore.home_team_code.upper()
        else:
          teamAbbr = boxscore.away_team_code.upper()
        '''
        for battingNode in boxscoreChild.childNodes:
          if battingNode.nodeType == node.ELEMENT_NODE:
            if battingNode.tagName == "batter":
              batter = buildBoxscoreBatter(battingNode)
              batter.teamAbbr = teamAbbr
              if teamFlag == "home":
                boxscore.home_batters.append(batter)
              else:
                boxscore.away_batters.append(batter)
            if battingNode.tagName == "note":
              if teamFlag == "home":
                boxscore.home_batter_notes.append(battingNode.firstChild.wholeText)
              else:
                boxscore.away_batter_notes.append(battingNode.firstChild.wholeText)
            if battingNode.tagName == "text_data":
              if teamFlag == "home":
                boxscore.home_batter_text_data = battingNode.firstChild.wholeText
              else:
                boxscore.away_batter_text_data = battingNode.firstChild.wholeText
      if boxscoreChild.tagName == "pitching":
        teamAbbr = ""
        teamFlag = boxscoreChild.getAttribute("team_flag")
        '''
        if teamFlag == "home":
          teamAbbr = boxscore.home_team_code.upper()
        else:
          teamAbbr = boxscore.away_team_code.upper()
        '''
        for pitcherNode in boxscoreChild.childNodes:
          if pitcherNode.nodeType == node.ELEMENT_NODE:
            if pitcherNode.tagName == "pitcher":
              pitcher = buildBoxscorePitcher(pitcherNode)
              pitcher.teamAbbr = teamAbbr
              #pitchers.append(pitcher)
              if teamFlag == "home":
                boxscore.home_pitchers.append(pitcher)
              else:
                boxscore.away_pitchers.append(pitcher)
      if boxscoreChild.tagName == "game_info":
        boxscore.game_info = boxscoreChild.childNodes[0].nodeValue

  return boxscore

'''
'''
def buildBoxscoreBatter(node):
  batter = BoxscoreBatter(node.getAttribute("id"))
  batter.name = node.getAttribute("name")
  batter.pos = node.getAttribute("pos")
  batter.bo = node.getAttribute("bo")
  batter.po = node.getAttribute("po")
  batter.hr = node.getAttribute("hr")
  batter.t = node.getAttribute("t")
  batter.a = node.getAttribute("a")
  batter.h = node.getAttribute("h")
  batter.bb = node.getAttribute("bb")
  batter.rbi = node.getAttribute("rbi")
  batter.so = node.getAttribute("so")
  batter.ab = node.getAttribute("ab")
  batter.r = node.getAttribute("r")
  batter.e = node.getAttribute("e")
  batter.d = node.getAttribute("d")
  batter.hbp = node.getAttribute("hbp")
  batter.sf = node.getAttribute("sf")
  batter.lob = node.getAttribute("lob")
  batter.fldg = node.getAttribute("fldg")
  batter.avg = node.getAttribute("avg")
  batter.note = node.getAttribute("note")
  return batter

'''
'''
def buildBoxscorePitcher(node):
  pitcher = BoxscorePitcher(node.getAttribute("id"))
  pitcher.name = node.getAttribute("name")
  pitcher.pos = node.getAttribute("pos")
  pitcher.out = node.getAttribute("out")
  pitcher.ip = str( (int(node.getAttribute("out")) / 3) ) + "." + str( (int(node.getAttribute("out")) % 3) )
  pitcher.bf = node.getAttribute("bf")
  pitcher.hr = node.getAttribute("hr")
  pitcher.bb = node.getAttribute("bb")
  pitcher.so = node.getAttribute("so")
  pitcher.er = node.getAttribute("er")
  pitcher.r = node.getAttribute("r")
  pitcher.h = node.getAttribute("h")
  pitcher.w = node.getAttribute("w")
  pitcher.l = node.getAttribute("l")
  pitcher.era = node.getAttribute("era")
  pitcher.note = node.getAttribute("note")
  return pitcher

'''
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

def buildInning(node):
  inning = Inning(node.getAttribute("num"))
  inning.next = node.getAttribute("next")
  inning.top_atbats = []
  inning.bottom_atbats = []
  for inningTypeNode in node.childNodes:
    if inningTypeNode.nodeType == node.ELEMENT_NODE:
      if inningTypeNode.tagName == "top":
        for innEventNode in inningTypeNode.childNodes:
          if innEventNode.nodeType == node.ELEMENT_NODE:
            inningEvent = InningEvent(innEventNode.getAttribute("des"))
            inningEvent.b = innEventNode.getAttribute("b")
            inningEvent.s = innEventNode.getAttribute("s")
            inningEvent.o = innEventNode.getAttribute("o")
            inningEvent.event = innEventNode.getAttribute("event")
            if innEventNode.tagName == "action":
              inningEvent.type = "action"
              inningEvent.player = innEventNode.getAttribute("player")
              inningEvent.pitch = innEventNode.getAttribute("pitch")
            if innEventNode.tagName == "atbat":
              inningEvent.type = "atbat"
              inningEvent.num = innEventNode.getAttribute("num")
              inningEvent.batter = innEventNode.getAttribute("batter")
              inningEvent.stand = innEventNode.getAttribute("stand")
              inningEvent.b_height = innEventNode.getAttribute("b_height")
              inningEvent.pitcher = innEventNode.getAttribute("pitcher")
              inningEvent.p_throws = innEventNode.getAttribute("p_throws")
              inningEvent.score = innEventNode.getAttribute("score")
              inningEvent.pitches = []
              for pitchNode in innEventNode.childNodes:
                if pitchNode.nodeType == node.ELEMENT_NODE:
                  if pitchNode.tagName == "pitch":
                    inningEvent.pitches.append(buildPitch(pitchNode))
                  #if pitchNode.tagName == "runner":
                    #todo: do i want this?
                    #inningEvent.pitches
          inning.top_atbats.append(inningEvent)
      if inningTypeNode.tagName == "bottom":
        for innEventNode in inningTypeNode.childNodes:
          inningEvent = {}
          if innEventNode.nodeType == node.ELEMENT_NODE:
            inningEvent = InningEvent(innEventNode.getAttribute("des"))
            inningEvent.b = innEventNode.getAttribute("b")
            inningEvent.s = innEventNode.getAttribute("s")
            inningEvent.o = innEventNode.getAttribute("o")
            inningEvent.event = innEventNode.getAttribute("event")
            if innEventNode.tagName == "action":
              inningEvent.type = "action"
              inningEvent.player = innEventNode.getAttribute("player")
              inningEvent.pitch = innEventNode.getAttribute("pitch")
            if innEventNode.tagName == "atbat":
              inningEvent.type = "atbat"
              inningEvent.num = innEventNode.getAttribute("num")
              inningEvent.batter = innEventNode.getAttribute("batter")
              inningEvent.stand = innEventNode.getAttribute("stand")
              inningEvent.b_height = innEventNode.getAttribute("b_height")
              inningEvent.pitcher = innEventNode.getAttribute("pitcher")
              inningEvent.p_throws = innEventNode.getAttribute("p_throws")
              inningEvent.score = innEventNode.getAttribute("score")
              inningEvent.pitches = []
              for pitchNode in innEventNode.childNodes:
                if pitchNode.nodeType == node.ELEMENT_NODE:
                  if pitchNode.tagName == "pitch":
                    inningEvent.pitches.append(buildPitch(pitchNode))
                  #if pitchNode.tagName == "runner":
                    #todo: do i want this?
                    #inningEvent.pitches
          inning.bottom_atbats.append(inningEvent)
  return inning