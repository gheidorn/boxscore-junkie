#    This work is licensed under the Creative Commons Attribution 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ or 
#    send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
#    California, 94105, USA.
#    
#    models.py declares the object model to be used in the application
#    
#    $Id$
class GameDay():
  def __init__ (self, day, month, year):
    self.day = day
    self.month = month
    self.year = year

class Game():
  def __init__ (self, id):
    self.id = id

class GameStatus():
  def __init__ (self, status):
    self.status = status

class GameBatter():
  def __init__ (self, id):
    self.id = id

class GamePitcher():
  def __init__ (self, id):
    self.id = id

class GameProbablePitcher():
  def __init__ (self, id):
    self.id = id

class GameOpposingPitcher():
  def __init__ (self, id):
    self.id = id

class GameHomeRuns():
  def __init__ (self):
    self.homeruns = []

class GameHomeRun():
  def __init__ (self, id):
    self.id = id

class GameWinningPitcher():
  def __init__ (self, id):
    self.id = id

class GameLosingPitcher():
  def __init__ (self, id):
    self.id = id

class GameSavePitcher():
  def __init__ (self, id):
    self.id = id

class GameLinescore():
  def __init__ (self):
    self.innings = []

class GameLinescoreInning():
  def __init__ (self, num):
    self.num = num

class GameLinescoreRuns():
  def __init__ (self):
    self.home = ""
    self.away = ""
    self.diff = ""

class GameLinescoreHits():
  def __init__ (self):
    self.home = ""
    self.away = ""

class GameLinescoreErrors():
  def __init__ (self):
    self.home = ""
    self.away = ""

class GameRunnersOnBase():
  def __init__ (self,status):
    self.status = status

class GameRunnerOnBase():
  def __init__ (self, id):
    self.id = id

class GameOnDeck():
  def __init__ (self, id):
    self.id = id

class GameInHole():
  def __init__ (self, id):
    self.id = id

class GamePBP():
  def __init__ (self, last_play):
    self.last_play = last_play

class GameLinks():
  def __init__ (self, tv_station):
    self.tv_station = tv_station

class GameAlerts():
  def __init__ (self, type):
    self.type = type

class Boxscore():
  def __init__ (self, id):
    self.id = id

class BoxscorePitcher():
  def __init__ (self, id):
    self.id = id

class BoxscoreBatter():
  def __init__ (self, id):
    self.id = id

class PitcherPBP():
  def __init__ (self, id):
    self.id = id

class BatterPBP():
  def __init__ (self, id):
    self.id = id

class AtBat():
  def __init__ (self, num):
    self.num = num

class Pitch():
  def __init__ (self, id):
    self.id = id

'''
Originally designed for fetching an inning's play-by-play and pitch-by-pitch data.
'''
class Inning():
  def __init__ (self, num):
    self.num = num

class InningEvent():
  def __init__ (self, des):
    self.des = des

'''
Design to represent the video highlights for a given game.
'''
class Highlights():
  def __init__ (self, gid):
    self.gid = gid

class Media():
  def __init__ (self, id):
    self.id = id

class MediaUrl():
  def __init__ (self, id):
    self.id = id

class MediaKeyword():
  def __init__ (self, type):
    self.type = type
'''
status
linescore
  inning..n away/home  * in P, <inning away=""/>
  r away/home/diff
  h away/home
  e away/home
batter id/ab/h/last/first/number/avg/hr/rbi
pitcher id/ip/er/era/wins/losses/last/first/number
opposing_pitcher id/era/wins/losses/last/first/number
pbp last
ondeck
inhole
homeruns
  player id/last/first/number/hr/std_hr/inning/runners/team_code
runners_on_base
  <runners_on_base status="2">
    <runner_on_2b id="455759" last="Young" first="Chris" number="24"/>
  </runners_on_base>
  <runners_on_base status="1">
    <runner_on_1b id="455759" last="Young" first="Chris" number="24"/>
  </runners_on_base>
links
alerts

winning_pitcher id/last/first/number/era/wins/losses
losing_pitcher id/last/first/number/era/wins/losses
save_pitcher id/last/first/number/era/wins/losses/saves


<status status="Warmup" ind="PW" reason="" inning="1" top_inning="Y" b="0" s="0" o="0"/>
'''