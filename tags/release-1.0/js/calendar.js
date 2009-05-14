// Global variables
var CAL_DAYS_LABELS = ['Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa'];
var CAL_MONTHS_LABELS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var CAL_DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
var CAL_CURRENT_DATE = new Date();
CAL_CURRENT_DATE.setFullYear(CALENDAR_YEAR, 2, 30);

function initPage() {
	/*
	var pageHeader = document.getElementById("page-header");
	pageHeader.innerHTML = CAL_CURRENT_DATE.getFullYear() + " Baseball Season";
	*/
	
	// iterate from March to October ... the MLB season
	for(var i = 2; i<10; i++) {
	  var calObj = new Calendar(i, null);
	  calObj.generateHTML();
	  var calDiv = document.getElementById("month" + (i+1));
	  calDiv.innerHTML = calObj.getHTML();
	}
}

function Calendar(month, year) {
  this.month = (isNaN(month) || month === null) ? CAL_CURRENT_DATE.getMonth() : month;
  this.year  = (isNaN(year) || year === null) ? CAL_CURRENT_DATE.getFullYear() : year;
  this.html = '';
}

Calendar.prototype.generateHTML = function(){
  // get first day of month
  var firstDay = new Date(this.year, this.month, 1);
  var startingDay = firstDay.getDay();
  
  // find number of days in month
  var monthLength = CAL_DAYS_IN_MONTH[this.month];
  
  // compensate for leap year
  if (this.month == 1) { // February only!
    if((this.year % 4 === 0 && this.year % 100 !== 0) || this.year % 400 === 0){
      monthLength = 29;
    }
  }
  
  // do the header
  var monthName = CAL_MONTHS_LABELS[this.month];
  var html = "<table class=\"calendar-table\">";
  html += "<tr><th colspan=\"7\">";
  html +=  monthName; // + "&nbsp;" + this.year;
  html += "<\/th><\/tr>";
  html += "<tr class=\"calendar-header\">";
  for(var i = 0; i <= 6; i++ ){
    html += "<td class=\"calendar-header-day\">";
    html += CAL_DAYS_LABELS[i];
    html += "<\/td>";
  }
  html += "<\/tr><tr>";

  // fill in the days
  var day = 1;
  // this loop is for is weeks (rows)
  for (var j = 0; j < 9; j++) {
    // this loop is for weekdays (cells)
    for (var k = 0; k <= 6; k++) { 
      var cssClass = "valid-date";
      //alert("currentDate: " +CAL_CURRENT_DATE.getMonth()+ "\nthis.month: "+this.month);
/*
      if(this.month == 2 && 
        (day == 25 || day == 26 || day == 30 || day == 31)) {
        cssClass = "valid-date";
      } else if(this.month > 2 && this.month < CAL_CURRENT_DATE.getMonth()) {
        cssClass = "valid-date";
      } else if(this.month == CAL_CURRENT_DATE.getMonth() && day < CAL_CURRENT_DATE.getDate()) {
        cssClass = "valid-date";
      } else if(this.month == CAL_CURRENT_DATE.getMonth() && day == CAL_CURRENT_DATE.getDate()) {
        cssClass = "current-date";
      }
*/
      
      if (day <= monthLength && (j > 0 || k >= startingDay)) {
        html += "<td class=\""+cssClass+"\" ";
        
        if(cssClass == "current-date" || cssClass == "valid-date") {
            html += "onclick=\"gotoScoreboard('" + this.year + "','" + (this.month+1) + "','" + day + "')\"";
        } 
        html += ">" + day;
        day++;
      } else {
        html += "<td class=\"empty-date\">&nbsp;";
      }
      html += "<\/td>";
    }
    // stop making rows if we've run out of days
    if (day > monthLength) {
      break;
    } else {
      html += "<\/tr><tr>";
    }
  }
  html += "<\/tr><\/table>";
  this.html = html;
};

Calendar.prototype.getHTML = function() {
  return this.html;
};

function gotoScoreboard(year, month, day) {
  var newUrl = '/scoreboard?year=' + year + '&month=' + month + '&day=' + day;
  window.location = newUrl;
}