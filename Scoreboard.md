## Introduction ##
There is an assumed format that gets tweaked now and then as new stats are popularized, such as On-Base Percentage (OBP) and On-Base Plus Slugging (OPS) in recent years.  This page describes that general "human-readable" format and then the XML/JSON formats provided by MLBAM for the Scoreboard.

## What is a Scoreboard? ##
The scoreboard refers to the game scores across the Major Leagues for a given day.

## Scoreboard XML ##
If you are better versed in reading XSDs, here is the [Scoreboard XSD](http://boxscore-junkie.googlecode.com/files/scoreboard.xsd) I reverse-engineered using Castor.

Here is a skeleton identifying each of the nodes in this schema.
```
<games>
  <game>
    <status>
    <linescore>
      <inning>
      <r>
      <h>
      <e>
    <homeruns>
      <player>
    <winning_pitcher>
    <losing_pitcher>
    <save_pitcher>
    <links>
    <game_media>
      <media>
```

And a sample game fleshed out from June 20th, 2009.

```

http://gd2.mlb.com/components/game/mlb/year_2009/month_06/day_20/master_scoreboard.xml

<game id="2009/06/20/clemlb-chnmlb-1" ampm="PM" venue="Wrigley Field" game_pk="245214" time="1:05" time_zone="ET" game_type="R" resume_date="" 
  away_name_abbrev="CLE" home_name_abbrev="CHC" away_code="cle" away_file_code="cle" away_team_id="114" away_team_city="Cleveland" away_team_name="Indians" 
  away_division="C" away_league_id="103" away_sport_code="mlb" home_code="chn" home_file_code="chc" home_team_id="112" home_team_city="Chi Cubs" 
  home_team_name="Cubs" home_division="C" home_league_id="104" home_sport_code="mlb" day="SAT" gameday_sw="E"
  away_games_back="10.0" home_games_back="3.5" away_games_back_wildcard="9.0" home_games_back_wildcard="2.5" venue_w_chan_loc="USIL0225"
  gameday="2009_06_20_clemlb_chnmlb_1" away_win="29" away_loss="41" home_win="33" home_loss="31" league="AN">
  <status status="Final" ind="F" reason="" inning="13" top_inning="N" b="0" s="0" o="1"/>
  <linescore>
    <inning away="1" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="1" home="2"/>
    <inning away="1" home="2"/>
    <inning away="1" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="0" home="0"/>
    <inning away="1" home="2"/>
    <r away="5" home="6" diff="1"/>
    <h away="10" home="12"/>
    <e away="2" home="0"/>
  </linescore>
  <home_runs>
    <player id="425509" last="Peralta" first="Jhonny" number="2" hr="1" std_hr="3" inning="6" runners="0" team_code="cle"/>
    <player id="117601" last="Lee" first="Derrek" number="25" hr="1" std_hr="11" inning="5" runners="1" team_code="chn"/>
    <player id="472528" last="Valbuena" first="Luis" number="1" hr="2" std_hr="4" inning="13" runners="0" team_code="cle"/>
    <player id="451687" last="Hoffpauir" first="Micah" number="6" hr="1" std_hr="5" inning="6" runners="1" team_code="chn"/>
  </home_runs>
  <winning_pitcher id="456029" last="Patton" first="David" number="54" era="5.75" wins="3" losses="1"/>
  <losing_pitcher id="134268" last="Wood" first="Kerry" number="34" era="5.47" wins="2" losses="3"/>
  <save_pitcher id="" last="" first="" number="" era="0" wins="0" losses="0" saves="0"/>
  <links wrapup="javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'wrap',lurl:'/news/wrap.jsp?ymd=20090620&content_id=5433024&vkey=wrapup2005&fext=.jsp&c_id=mlb'}))" 
    home_preview="javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'preview',lurl:'/news/article.jsp?ymd=20090619&content_id=5414850&vkey=news_chc&fext=.jsp&c_id=chc'}))" 
    away_preview="javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'preview',lurl:'/news/article.jsp?ymd=20090619&content_id=5414838&vkey=news_cle&fext=.jsp&c_id=cle'}))" 
    preview="" tv_station="WGN"/>
  <game_media>
    <media type="game" calendar_event_id="14-245214-2009-06-20" start="2009-06-20T13:05:00-0400" title="CLE @ CHC" media_state="media_archive"/>
  </game_media>
</game>
```

### Scoreboard JSON ###
Here is the same game represented in JSON.
```

http://gd2.mlb.com/components/game/mlb/year_2009/month_06/day_20/master_scoreboard.json

        {
            "game_type": "R",
            "game_media": {"media": {
                "title": "CLE @ CHC",
                "media_state": "media_archive",
                "start": "2009-06-20T13:05:00-0400",
                "calendar_event_id": "14-245214-2009-06-20",
                "type": "game"
            }},
            "away_games_back_wildcard": "9.0",
            "linescore": {
                "e": {
                    "home": "0",
                    "away": "2"
                },
                "r": {
                    "home": "6",
                    "away": "5",
                    "diff": "1"
                },
                "inning": [
                    {
                        "home": "0",
                        "away": "1"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "2",
                        "away": "1"
                    },
                    {
                        "home": "2",
                        "away": "1"
                    },
                    {
                        "home": "0",
                        "away": "1"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "0",
                        "away": "0"
                    },
                    {
                        "home": "2",
                        "away": "1"
                    }
                ],
                "h": {
                    "home": "12",
                    "away": "10"
                }
            },
            "venue_w_chan_loc": "USIL0225",
            "away_team_name": "Indians",
            "home_runs": {"player": [
                {
                    "std_hr": "3",
                    "hr": "1",
                    "id": "425509",
                    "last": "Peralta",
                    "team_code": "cle",
                    "inning": "6",
                    "runners": "0",
                    "number": "2",
                    "first": "Jhonny"
                },
                {
                    "std_hr": "11",
                    "hr": "1",
                    "id": "117601",
                    "last": "Lee",
                    "team_code": "chn",
                    "inning": "5",
                    "runners": "1",
                    "number": "25",
                    "first": "Derrek"
                },
                {
                    "std_hr": "4",
                    "hr": "2",
                    "id": "472528",
                    "last": "Valbuena",
                    "team_code": "cle",
                    "inning": "13",
                    "runners": "0",
                    "number": "1",
                    "first": "Luis"
                },
                {
                    "std_hr": "5",
                    "hr": "1",
                    "id": "451687",
                    "last": "Hoffpauir",
                    "team_code": "chn",
                    "inning": "6",
                    "runners": "1",
                    "number": "6",
                    "first": "Micah"
                }
            ]},
            "home_name_abbrev": "CHC",
            "id": "2009/06/20/clemlb-chnmlb-1",
            "time": "1:05",
            "ampm": "PM",
            "home_team_name": "Cubs",
            "home_division": "C",
            "home_team_city": "Chi Cubs",
            "gameday_sw": "E",
            "away_win": "29",
            "home_games_back_wildcard": "2.5",
            "save_pitcher": {
                "id": "",
                "last": "",
                "saves": "0",
                "losses": "0",
                "era": "0",
                "number": "",
                "first": "",
                "wins": "0"
            },
            "away_team_id": "114",
            "status": {
                "top_inning": "N",
                "s": "0",
                "b": "0",
                "reason": "",
                "ind": "F",
                "status": "Final",
                "o": "1",
                "inning": "13"
            },
            "home_loss": "31",
            "home_games_back": "3.5",
            "home_code": "chn",
            "home_sport_code": "mlb",
            "away_sport_code": "mlb",
            "home_win": "33",
            "links": {
                "wrapup": "javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'wrap',lurl:'/news/wrap.jsp?ymd=20090620&content_id=5433024&vkey=wrapup2005&fext=.jsp&c_id=mlb'}))",
                "preview": "",
                "home_preview": "javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'preview',lurl:'/news/article.jsp?ymd=20090619&content_id=5414850&vkey=news_chc&fext=.jsp&c_id=chc'}))",
                "away_preview": "javascript:void(launchGameday({gid:'2009_06_20_clemlb_chnmlb_1',mode:'preview',lurl:'/news/article.jsp?ymd=20090619&content_id=5414838&vkey=news_cle&fext=.jsp&c_id=cle'}))",
                "tv_station": "WGN"
            },
            "game_pk": "245214",
            "away_name_abbrev": "CLE",
            "league": "AN",
            "venue": "Wrigley Field",
            "away_games_back": "10.0",
            "home_file_code": "chc",
            "home_league_id": "104",
            "away_loss": "41",
            "time_zone": "ET",
            "away_league_id": "103",
            "resume_date": "",
            "away_file_code": "cle",
            "losing_pitcher": {
                "id": "134268",
                "last": "Wood",
                "losses": "3",
                "era": "5.47",
                "number": "34",
                "first": "Kerry",
                "wins": "2"
            },
            "home_team_id": "112",
            "day": "SAT",
            "away_team_city": "Cleveland",
            "away_code": "cle",
            "winning_pitcher": {
                "id": "456029",
                "last": "Patton",
                "losses": "1",
                "era": "5.75",
                "number": "54",
                "first": "David",
                "wins": "3"
            },
            "gameday": "2009_06_20_clemlb_chnmlb_1",
            "away_division": "C"
        }
```

## Copyright Information ##
The accounts, descriptions, data and presentation in the referring page (the "Materials") are proprietary content of MLB Advanced Media, L.P ("MLBAM").

Only individual, non-commercial, non-bulk use of the Materials is permitted and any other use of the Materials is prohibited without prior written authorization from MLBAM.

Authorized users of the Materials are prohibited from using the Materials in any commercial manner other than as expressly authorized by MLBAM.

[MLBAM Copyright Notice](http://gd2.mlb.com/components/copyright.txt)