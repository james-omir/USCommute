var states = ["Alabama","Alaska","Arizona","Arkansas","California",
"Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii",
"Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
"Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
"New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma",
"Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota",
"Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
"Wisconsin","Wyoming"];

var g = new Date();
var time = g.getTime();

function GetData(site) {
	var XMLReq = new XMLHttpRequest();

	XMLReq.open( "GET", site, false )
	XMLReq.send();
	return XMLReq.responseText
}

function Parse(content, start, stop, margin){
	var first = content.indexOf(start);
	var difference = content.substring(first,first+start.length + margin);
	var second = difference.indexOf(stop) + first;
	
	var result = content.substring(first + start.length,second);
	var content = [result, second]
	return content
}

function getWeather(){
	var margin = 20;
	var weather = GetData("https://weather.com/weather/today/l/40.36,-74.04?par=google");
	var weatherS = '<span data-testid="TemperatureValue" class="CurrentConditions--tempValue--3a50n">';
	var weatherE = '</span>';
	var weatherResult = Parse(weather,weatherS,weatherE, margin)[0];
	document.getElementById("weatherBlock").innerHTML = weatherResult;
}


getWeather();

function getNews(){
	margin = 200;
	linkMargin = 500;
	var news = GetData("https://www.nj.com/");
	var newsS = 'data-ga-content-type="article" data-linktype="headline">';
	var newsE = '</a>'
	var linkS = 'href="'
	var linkE = '" data-ga';
	
	
	
	var newsResult = Parse(news,newsS,newsE, margin);
	var bl = document.getElementById('newsBlock1');
	bl.innerHTML = newsResult[0];
	var linkRes = Parse(news.substring(newsResult[1]-linkMargin), linkS, linkE, linkMargin);
	bl.href = linkRes[0]

	var newLoc = news.substring(newsResult[1]);
	newsResult = Parse(newLoc,newsS,newsE, margin);
	var bl = document.getElementById('newsBlock2');
	bl.innerHTML = newsResult[0];
	linkRes = Parse(news.substring(newsResult[1]-linkMargin), linkS, linkE, linkMargin);
	bl.href = linkRes[0]
	newLoc = newLoc.substring(newsResult[1]);

	newsResult = Parse(newLoc,newsS,newsE, margin);
	var bl = document.getElementById('newsBlock3');
	bl.innerHTML = newsResult[0];
	linkRes = Parse(news.substring(newsResult[1]-linkMargin), linkS, linkE, linkMargin);
	bl.href = linkRes[0]
	newLoc = newLoc.substring(newsResult[1]);

	newsResult = Parse(newLoc,newsS,newsE, margin);
	var bl = document.getElementById('newsBlock4');
	bl.innerHTML = newsResult[0];
	linkRes = Parse(news.substring(newsResult[1]-linkMargin), linkS, linkE, linkMargin);
	bl.href = linkRes[0]
}

getNews();




