/*
Deepbox Live functions
*/


/**
 * Builds a table of atbats from a pitchers outing.
 */
function fetchPBPPitcher(thisObj) {
	if(thisObj.item(thisObj.selectedIndex).value === "") {
		return;
	}
  var pbpDisplay = document.getElementById('pbp-display');
  pbpDisplay.innerHTML = '<img src="/img/wait30.gif" />';
  var callback = {
    success: function (o) {
      var rootNode = o.responseXML.getElementsByTagName('player').item(0);
      var atbats = [];
      var firstLevelNodes = rootNode.childNodes;
      if(firstLevelNodes !== null) {  // skip pinch runners and defensive subs
        for(var i = 0; i < firstLevelNodes.length; i++) {
          var curLvl1Item = firstLevelNodes.item(i);
          if(curLvl1Item.nodeType === Node.ELEMENT_NODE && curLvl1Item.tagName === "atbat") {
            var atbat = {};
            atbat.inning = curLvl1Item.attributes.getNamedItem('inning').value;
            if(atbat.inning === 1) {
              atbat.inningLbl = atbat.inning + "st";
            } else if(atbat.inning === 2) {
              atbat.inningLbl = atbat.inning + "nd";
            } else if(atbat.inning === 3) {
              atbat.inningLbl = atbat.inning + "rd";
            } else {
              atbat.inningLbl = atbat.inning + "th";
            }
            atbat.num = curLvl1Item.attributes.getNamedItem('num').value;
            atbat.batterId = curLvl1Item.attributes.getNamedItem('batter').value;
            atbat.pitcherId = curLvl1Item.attributes.getNamedItem('pitcher').value;
            atbat.des = curLvl1Item.attributes.getNamedItem('des').value;
            atbat.event = curLvl1Item.attributes.getNamedItem('event').value;
            atbat.pitches = [];
            var secondLevelNodes = curLvl1Item.childNodes;
            for(var j = 0; j < secondLevelNodes.length; j++) {
              var curLvl2Item = secondLevelNodes.item(j);
              var pitch = {};
              if(curLvl2Item.tagName === "pitch") {
                pitch.id = curLvl2Item.attributes.getNamedItem('id').value;
                pitch.des = curLvl2Item.attributes.getNamedItem('des').value;
                pitch.type = curLvl2Item.attributes.getNamedItem('type').value;
                pitch.x = curLvl2Item.attributes.getNamedItem('x').value;
                pitch.y = curLvl2Item.attributes.getNamedItem('y').value;
                // check if pitch f/x data was recorded
                if(curLvl2Item.attributes.getNamedItem('sv_id') !== null) {
                  pitch.sv_id = curLvl2Item.attributes.getNamedItem('sv_id').value;
                  pitch.start_speed = curLvl2Item.attributes.getNamedItem('start_speed').value;
                  pitch.end_speed = curLvl2Item.attributes.getNamedItem('end_speed').value;
                  pitch.sz_top = curLvl2Item.attributes.getNamedItem('sz_top').value;
                  pitch.sz_bot = curLvl2Item.attributes.getNamedItem('sz_bot').value;
                  pitch.pfx_x = curLvl2Item.attributes.getNamedItem('pfx_x').value;
                  pitch.pfx_z = curLvl2Item.attributes.getNamedItem('pfx_z').value;
                  pitch.px = curLvl2Item.attributes.getNamedItem('px').value;
                  pitch.pz = curLvl2Item.attributes.getNamedItem('pz').value;
                  pitch.x0 = curLvl2Item.attributes.getNamedItem('x0').value;
                  pitch.y0 = curLvl2Item.attributes.getNamedItem('y0').value;
                  pitch.z0 = curLvl2Item.attributes.getNamedItem('z0').value;
                  pitch.vx0 = curLvl2Item.attributes.getNamedItem('vx0').value;
                  pitch.vy0 = curLvl2Item.attributes.getNamedItem('vy0').value;
                  pitch.vz0 = curLvl2Item.attributes.getNamedItem('vz0').value;
                  pitch.ax = curLvl2Item.attributes.getNamedItem('ax').value;
                  pitch.ay = curLvl2Item.attributes.getNamedItem('ay').value;
                  pitch.az = curLvl2Item.attributes.getNamedItem('az').value;
                  pitch.break_y = curLvl2Item.attributes.getNamedItem('break_y').value;
                  pitch.break_angle = curLvl2Item.attributes.getNamedItem('break_angle').value;
                  pitch.break_length = curLvl2Item.attributes.getNamedItem('break_length').value;
                  pitch.pitch_type = curLvl2Item.attributes.getNamedItem('pitch_type').value;
                  pitch.type_confidence = curLvl2Item.attributes.getNamedItem('type_confidence').value;
                  pitch.pitchOut = false;
                }
              } else if(curLvl2Item.tagName == "po") {
                pitch.pickoff = true;
                pitch.des = curLvl2Item.attributes.getNamedItem('des').value;
              }
              atbat.pitches[j] = pitch;
            }
            atbats[i] = atbat;
          }
        }
      }    
      
      var pitches = { total: 0, na: 0, FA: 0, FS:0, FF: 0, FC: 0, CU: 0, CH: 0, SI: 0, SL: 0, KN: 0 };
      var pitchSpeed = { FA: [], FS: [], FF: [], FC: [], CU: [], CH: [], SI: [], SL: [], KN: [] };
      var pitchBreak = { FA: [], FS: [], FF: [], FC: [], CU: [], CH: [], SI: [], SL: [], KN: [] };
      var pitchReleasePoint = { FA: [], FS: [], FF: [], FC: [], CU: [], CH: [], SI: [], SL: [], KN: [] };
      
      var pbpDisplayHTML = "<table>";
      var inningCtr = 0;
      var releasePoint_y0 = 0;
      for(var k = 0; k < atbats.length; k++) {
        if(atbats[k].inning != inningCtr) {
          inningCtr = atbats[k].inning;
          pbpDisplayHTML += "<tr><td class=\"divider\">" + atbats[k].inningLbl + "<\/td><\/tr>";
        }
        pbpDisplayHTML += "<tr><td><table class=\"pitch-sequence\"><tr><th>&nbsp;<\/th><th>REL<\/th><th>SPD<\/th><th>BRK<\/th><th>PFX<\/th><th>PITCH<\/th><th>RESULT<\/th><\/tr>";
        var pitchCtr = 0;
        for(var m = 0; m < atbats[k].pitches.length; m++) {
        	releasePoint_y0 = atbats[k].pitches[m].y0; // TODO not efficient; replace with single XML dive at some point
          if(atbats[k].pitches[m].pickoff) {
            pbpDisplayHTML += "<tr><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td class=\"pitch\">" + atbats[k].pitches[m].des + "<\/td><\/tr>";
          } else {
            pitchCtr++;
            pitches.total++;
            if(atbats[k].pitches[m].z0 === undefined) {
            	pitches.na++;
            	pbpDisplayHTML += "<tr><td class=\"td-num\">"+pitchCtr+"<\/td><td class=\"td-spd\">n/a<\/td><td class=\"td-spd\">n/a<\/td><td class=\"td-brk\">n/a<\/td><td class=\"td-pfx\">n/a<\/td><td class=\"td-pitch\">n/a<\/td><td class=\"td-result\">"+atbats[k].pitches[m].des + "<\/td><\/tr>";
           	} else {
           		pitches[atbats[k].pitches[m].pitch_type]++;
           		pitchSpeed[atbats[k].pitches[m].pitch_type].push(parseFloat(atbats[k].pitches[m].start_speed));
           		pitchBreak[atbats[k].pitches[m].pitch_type].push(parseFloat(atbats[k].pitches[m].break_length));
           		pitchReleasePoint[atbats[k].pitches[m].pitch_type].push(parseFloat(atbats[k].pitches[m].z0));
            	pbpDisplayHTML += "<tr><td class=\"td-num\">"+pitchCtr+"<\/td><td class=\"td-spd\">"+atbats[k].pitches[m].z0+"<\/td><td class=\"td-spd\">"+atbats[k].pitches[m].start_speed+"<\/td><td class=\"td-brk\">"+atbats[k].pitches[m].break_length+"<\/td><td class=\"td-pfx\">"+atbats[k].pitches[m].pfx_x+"<\/td><td class=\"td-pitch\">"+atbats[k].pitches[m].pitch_type+"<\/td><td class=\"td-result\">"+atbats[k].pitches[m].des + "<\/td><\/tr>";
            }
          }
        }
        pbpDisplayHTML += "<tr><td colspan=\"7\" class=\"pitch-event\">" + atbats[k].des + "<\/td><\/tr>";
        pbpDisplayHTML += "<\/table><\/td><\/tr>";
      }
      pbpDisplayHTML += "<\/table>";
      
      
      var intro = "<p>Pitch f/x measuring release point at "+releasePoint_y0+" feet.<br \/>Operator was lazy "+pitches.na+" times!<br \/>";
      
      for(var p in pitches) {
      	if(pitches[p] > 0) {
      		intro += pitches[p]+" "+ p + " ";
      	}
    	}
    	
      intro += "<br \/>Speed: ";
      
      
      var compare = function(a,b){
				return a-b;
			};
      
      for(var s in pitchSpeed) {
      	if(pitches[s] !== 0) {
      		pitchSpeed[s].sort(compare);
      		intro += pitchSpeed[s][pitchSpeed[s].length-1]+"/"+pitchSpeed[s][0]+" "+s+" ";
      	}
    	}

			intro += "<br \/>Break: ";
			
      for(var b in pitchBreak) {
      	if(pitches[b] !== 0) {
      		pitchBreak[b].sort(compare);
      		intro += pitchBreak[b][pitchBreak[b].length-1]+"/"+pitchBreak[b][0]+" "+b+" ";
      	}
    	}
      
      intro += "<br \/>Release: ";
      
      for(var rp in pitchReleasePoint) {
      	if(pitches[rp] !== 0) {
      		pitchReleasePoint[rp].sort(compare);
      		intro += pitchReleasePoint[rp][pitchReleasePoint[rp].length-1]+"/"+pitchReleasePoint[rp][0]+" "+rp+" ";
      	}
    	}
      
      intro += "<\/p>";
      pbpDisplay.innerHTML = intro;
      pbpDisplay.innerHTML += pbpDisplayHTML;
    },
    failure: function(o) {
      alert("need better error handling [fetchPBPPitcher]");
    },
    argument: null
  };  
  var gameSelectObj = document.forms.gameForm.elements.game;
  var url = '/fetch/pbp-pitcher?year=' + YEAR + '&month=' + MONTH + '&day=' + DAY + '&game=' + gameSelectObj.item(gameSelectObj.selectedIndex).value + "&pid=" + thisObj.item(thisObj.selectedIndex).value;
  YAHOO.util.Connect.asyncRequest('GET', url, callback, null);
}
/**
 * Builds a table of atbats from a batters day at the plate.
 */
function fetchPBPBatter(thisObj) {
	if(thisObj.item(thisObj.selectedIndex).value === "") {
		return;
	}
  var pbpDisplay = document.getElementById('pbp-display');
  pbpDisplay.innerHTML = '<img src="/img/wait30.gif" />';
  var callback = {
    success: function (o) {
      var rootNode = o.responseXML.getElementsByTagName('player').item(0);
      var atbats = [];
      var firstLevelNodes = rootNode.childNodes;
      if(firstLevelNodes !== null) {  // skip pinch runners and defensive subs
        for(var i = 0; i < firstLevelNodes.length; i++) {
          var curLvl1Item = firstLevelNodes.item(i);
          if(curLvl1Item.nodeType == Node.ELEMENT_NODE && curLvl1Item.tagName == 'atbat') {
            var atbat = {};
            atbat.inning = curLvl1Item.attributes.getNamedItem('inning').value;
            if(atbat.inning === 1) {
              atbat.inningLbl = atbat.inning + "st";
            } else if(atbat.inning === 2) {
              atbat.inningLbl = atbat.inning + "nd";
            } else if(atbat.inning === 3) {
              atbat.inningLbl = atbat.inning + "rd";
            } else {
              atbat.inningLbl = atbat.inning + "th";
            }
            atbat.num = curLvl1Item.attributes.getNamedItem('num').value;
            atbat.batterId = curLvl1Item.attributes.getNamedItem('batter').value;
            atbat.pitcherId = curLvl1Item.attributes.getNamedItem('pitcher').value;
            atbat.des = curLvl1Item.attributes.getNamedItem('des').value;
            atbat.event = curLvl1Item.attributes.getNamedItem('event').value;
            atbat.pitches = [];
            var secondLevelNodes = curLvl1Item.childNodes;
            for(var j = 0; j < secondLevelNodes.length; j++) {
              var curLvl2Item = secondLevelNodes.item(j);
              var pitch = {};
              if(curLvl2Item.tagName === "pitch") {
                pitch.id = curLvl2Item.attributes.getNamedItem('id').value;
                pitch.des = curLvl2Item.attributes.getNamedItem('des').value;
                pitch.type = curLvl2Item.attributes.getNamedItem('type').value;
                pitch.x = curLvl2Item.attributes.getNamedItem('x').value;
                pitch.y = curLvl2Item.attributes.getNamedItem('y').value;
                // check if pitch f/x data was recorded
                if(curLvl2Item.attributes.getNamedItem('sv_id') !== null) {
                  pitch.sv_id = curLvl2Item.attributes.getNamedItem('sv_id').value;
                  pitch.start_speed = curLvl2Item.attributes.getNamedItem('start_speed').value;
                  pitch.end_speed = curLvl2Item.attributes.getNamedItem('end_speed').value;
                  pitch.sz_top = curLvl2Item.attributes.getNamedItem('sz_top').value;
                  pitch.sz_bot = curLvl2Item.attributes.getNamedItem('sz_bot').value;
                  pitch.pfx_x = curLvl2Item.attributes.getNamedItem('pfx_x').value;
                  pitch.pfx_z = curLvl2Item.attributes.getNamedItem('pfx_z').value;
                  pitch.px = curLvl2Item.attributes.getNamedItem('px').value;
                  pitch.pz = curLvl2Item.attributes.getNamedItem('pz').value;
                  pitch.x0 = curLvl2Item.attributes.getNamedItem('x0').value;
                  pitch.y0 = curLvl2Item.attributes.getNamedItem('y0').value;
                  pitch.z0 = curLvl2Item.attributes.getNamedItem('z0').value;
                  pitch.vx0 = curLvl2Item.attributes.getNamedItem('vx0').value;
                  pitch.vy0 = curLvl2Item.attributes.getNamedItem('vy0').value;
                  pitch.vz0 = curLvl2Item.attributes.getNamedItem('vz0').value;
                  pitch.ax = curLvl2Item.attributes.getNamedItem('ax').value;
                  pitch.ay = curLvl2Item.attributes.getNamedItem('ay').value;
                  pitch.az = curLvl2Item.attributes.getNamedItem('az').value;
                  pitch.break_y = curLvl2Item.attributes.getNamedItem('break_y').value;
                  pitch.break_angle = curLvl2Item.attributes.getNamedItem('break_angle').value;
                  pitch.break_length = curLvl2Item.attributes.getNamedItem('break_length').value;
                  pitch.pitch_type = curLvl2Item.attributes.getNamedItem('pitch_type').value;
                  pitch.type_confidence = curLvl2Item.attributes.getNamedItem('type_confidence').value;
                  pitch.pitchOut = false;
                }
              } else if(curLvl2Item.tagName == "po") {
                pitch.pickoff = true;
                pitch.des = curLvl2Item.attributes.getNamedItem('des').value;
              }
              atbat.pitches[j] = pitch;
          	}
        	}
      	}    
      }
      var pbpDisplayHTML = "<table>";
      var inningCtr = 0;
      for(var k = 0; k < atbats.length; k++) {
        if(atbats[k].inning != inningCtr) {
          inningCtr = atbats[k].inning;
          pbpDisplayHTML += "<tr><td class=\"divider\">" + atbats[k].inningLbl + "<\/td><\/tr>";
        }
        pbpDisplayHTML += "<tr><td><table class=\"pitch-sequence\"><tr><th>&nbsp;<\/th><th>REL<\/th><th>SPD<\/th><th>BRK<\/th><th>PFX<\/th><th>PITCH<\/th><th>RESULT<\/th><\/tr>";
        var pitchCtr = 0;
        for(var m = 0; m < atbats[k].pitches.length; m++) {
          if(atbats[k].pitches[m].pickoff) {
            pbpDisplayHTML += "<tr><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td>&nbsp;<\/td><td class=\"pitch\">" + atbats[k].pitches[m].des + "<\/td><\/tr>";
          } else {
            pitchCtr++;
            if(atbats[k].pitches[m].z0 === undefined) {
            	pbpDisplayHTML += "<tr><td class=\"td-num\">"+pitchCtr+"<\/td><td class=\"td-spd\">n/a<\/td><td class=\"td-spd\">n/a<\/td><td class=\"td-brk\">n/a<\/td><td class=\"td-pfx\">n/a<\/td><td class=\"td-pitch\">n/a<\/td><td class=\"td-result\">"+atbats[k].pitches[m].des + "<\/td><\/tr>";
           	} else {
           		pbpDisplayHTML += "<tr><td class=\"td-num\">"+pitchCtr+"<\/td><td class=\"td-spd\">"+atbats[k].pitches[m].z0+"<\/td><td class=\"td-spd\">"+atbats[k].pitches[m].start_speed+"<\/td><td class=\"td-brk\">"+atbats[k].pitches[m].break_length+"<\/td><td class=\"td-pfx\">"+atbats[k].pitches[m].pfx_x+"<\/td><td class=\"td-pitch\">"+atbats[k].pitches[m].pitch_type+"<\/td><td class=\"td-result\">"+atbats[k].pitches[m].des + "<\/td><\/tr>";
            }
          }
        }
        pbpDisplayHTML += "<tr><td colspan=\"7\" class=\"pitch-event\">" + atbats[k].des + "<\/td><\/tr>";
        pbpDisplayHTML += "<\/table><\/td><\/tr>";
      }
      pbpDisplayHTML += "<\/table>";
      pbpDisplay.innerHTML += pbpDisplayHTML;
    },
    failure: function(o) {
      alert("need better error handling [fetchPBPPitcher]");
    },
    argument: null
  };  
  var gameSelectObj = document.forms.gameForm.elements.game;
  var url = '/fetch/pbp-batter?year=' + YEAR + '&month=' + MONTH + '&day=' + DAY + '&game=' + gameSelectObj.item(gameSelectObj.selectedIndex).value + "&pid=" + thisObj.item(thisObj.selectedIndex).value;
  YAHOO.util.Connect.asyncRequest('GET', url, callback, null);
}
/**
 * Retrieves the active pitchers and batters in a particular game.
 */
function fetchBoxscore(gameObj) {
	var boxscore = document.getElementById('boxscore');
	if(GAMES[gameObj.item(gameObj.selectedIndex).value].status === "Preview") {
		boxscore.innerHTML = "<span class=\"error\">Lineups not yet available.<\/span>";
	} else {
	  boxscore.innerHTML = "<img src=\"/img/wait30.gif\" />";
	  var callback = {
	    success: function(o) {
	      var rootNode = o.responseXML.getElementsByTagName('boxscore').item(0);
	      var pitchersCtr = 0;
	      var battersCtr = 0;
	      var pitchers = [];
	      var batters = [];
	      var firstLevelNodes = rootNode.childNodes;
	      for(var i = 0; i < firstLevelNodes.length; i++) {
	        var curLvl1Item = firstLevelNodes.item(i);
	        if(curLvl1Item.nodeType == Node.ELEMENT_NODE) {
	        	var secondLevelNodes = curLvl1Item.childNodes;
	          if(curLvl1Item.tagName === "pitching") {
	            for(var j = 0; j < secondLevelNodes.length; j++) {
	              var curLvl2Item = secondLevelNodes.item(j);
	              if(curLvl2Item.tagName === "pitcher") {
	                var pitcher = {};
	                pitcher.id = curLvl2Item.attributes.getNamedItem('id').value;
	                pitcher.name = curLvl2Item.attributes.getNamedItem('name').value;
	                pitcher.pos = curLvl2Item.attributes.getNamedItem('pos').value;
	                var pitcherTeam = curLvl1Item.attributes.getNamedItem('team_flag').value;
	                if(pitcherTeam === "home") { // determine team
	                  pitcher.team = rootNode.attributes.getNamedItem('home_team_code').value;
	                } else {
	                  pitcher.team = rootNode.attributes.getNamedItem('away_team_code').value;
	                }
	                pitcher.line = curLvl2Item.attributes.getNamedItem('out').value + " outs, " + curLvl2Item.attributes.getNamedItem('bf').value + " bf ";
	                if(curLvl2Item.attributes.getNamedItem('note') !== null) {
	                  pitcher.line += curLvl2Item.attributes.getNamedItem('note').value;
	                }
	                pitchers[pitchersCtr++] = pitcher;
	              }
	            }
	          } else if(curLvl1Item.tagName === "batting") {
	            for(var k = 0; k < secondLevelNodes.length; k++) {
	              var batterNode = secondLevelNodes.item(k);
	              if(batterNode.tagName === "batter") {
	                var batter = {};
	                batter.id = batterNode.attributes.getNamedItem('id').value;
	                batter.name = batterNode.attributes.getNamedItem('name').value;
	                batter.pos = batterNode.attributes.getNamedItem('pos').value;
	                // determine team
	                var batterTeam = curLvl1Item.attributes.getNamedItem('team_flag').value;
	                if(batterTeam === "home") {
	                  batter.team = rootNode.attributes.getNamedItem('home_team_code').value;
	                } else {
	                  batter.team = rootNode.attributes.getNamedItem('away_team_code').value;
	                }
	                batter.line = batterNode.attributes.getNamedItem('h').value + "-" + batterNode.attributes.getNamedItem('ab').value + ", " + batterNode.attributes.getNamedItem('bb').value + "bb";
	                batters[battersCtr++] = batter;
	              }
	            }
	          }
	        }
	      }
	      var pitcherOptions = "<select name=\"pitcher\" onchange=\"fetchPBPPitcher(this)\"><option />";
	      for(var ii = 0; ii < pitchers.length; ii++) {
	        pitcherOptions += "<option value=\"" + pitchers[ii].id + "\">" + pitchers[ii].id + " - " + pitchers[ii].name + " - " + pitchers[ii].line + "<\/option>";
	      }
	      pitcherOptions += '<\/select>';
	      var batterOptions = "<select name=\"batter\" onchange=\"fetchPBPBatter(this)\"><option />";   
	      for(var jj = 0; jj < batters.length; jj++) {
	        batterOptions += "<option value=\"" + batters[jj].id + "\">" + batters[jj].name + " - " + batters[jj].line + "<\/option>";
	      }
	      batterOptions += '<\/select>';
	      boxscore.innerHTML = ""; // remove ajax indicator
	      var pitchersDiv = document.getElementById('pitchers');
	      pitchersDiv.innerHTML = pitcherOptions;
	      var battersDiv = document.getElementById('batters');
	      battersDiv.innerHTML = batterOptions;
	    },
	    failure: function(o) {
	      alert();
	    },
	    argument: null
	  };
	  var url = '/fetch/boxscore?year='+YEAR+'&month='+MONTH+'&day='+DAY+'&game='+gameObj.item(gameObj.selectedIndex).value;
	  YAHOO.util.Connect.asyncRequest('GET', url, callback, null);
	}
}