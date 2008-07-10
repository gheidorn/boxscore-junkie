#!/usr/bin/env python

from google.appengine.ext import db

class DBTeam(db.Model):
  id = db.IntegerProperty(required=True)
  name = db.StringProperty(required=True)
  code = db.StringProperty(required=True)
  file_code = db.StringProperty(required=True)
  abbrev = db.StringProperty(required=True)
  league = db.StringProperty(required=True)

class DBPlayer(db.Model):
  id = db.IntegerProperty(required=True)
  team_id = db.ReferenceProperty(DBTeam)
  first = db.StringProperty(required=True)
  last = db.StringProperty(required=True)
  num = db.IntegerProperty(required=True)
  boxname = db.StringProperty(required=True)
  rl = db.StringProperty(required=True)
  position = db.StringProperty(required=True)
  status = db.StringProperty(required=True)
'''
class Pitch(db.Model):
  gid = db.StringProperty(required=True)
  pitcherId = db.IntegerProperty(required=True)
  batterId = db.IntegerProperty(required=True)
  id = db.IntegerProperty(required=True)
  des = db.StringProperty(required=True)
  type = db.StringProperty(required=True)
  x = db.FloatProperty(required=True)
  y = db.FloatProperty(required=True)
  sv_id = db.StringProperty
  start_speed =  db.FloatProperty
  end_speed =  db.FloatProperty
  sz_top = db.FloatProperty
  sz_bot = db.FloatProperty
  pfx_x = db.FloatProperty
  pfx_z = db.FloatProperty
  px = db.FloatProperty
  pz = db.FloatProperty
  x0 = db.FloatProperty
  y0 = db.FloatProperty
  z0 = db.FloatProperty
  vx0 = db.FloatProperty
  vy0 = db.FloatProperty
  vz0 = db.FloatProperty
  ax = db.FloatProperty
  ay = db.FloatProperty
  az = db.FloatProperty
  break_y = db.FloatProperty
  break_angle = db.FloatProperty
  break_length = db.FloatProperty
  pitch_type = db.StringProperty
  type_confidence = db.FloatProperty
'''