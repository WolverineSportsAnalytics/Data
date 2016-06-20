var app = angular.module('WSAData', ['ngSanitize']);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
}]);



app.controller("mainController", ['$scope', '$http', '$location', '$window', function($scope, $http, $location) {
	var wsa = this;

	wsa.username = "";

	wsa.validate = function(inUsername, inPassword) 
	{
		wsa.username = inUsername;
		// create data object
		var data = {
			username: inUsername,
			password: inPassword
		};
		// send to database 
		var submit = $http.post('/api/login/', data);

		submit.success(function(response){
			console.log("Success: " + response.toString())
			window.location.replace('/data/')
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
}]);

app.controller("baseballController", ['$scope', '$http', '$location', '$window', function($scope, $http, $location) {
	var wsa = this;

	var rotowireTimesGet = $http.get('/api/baseballRotowireTimes');

	rotowireTimesGet.success(function(response){
		console.log("Success getting Rotowire times");
		wsa.rotowireTimes = response;
	});
	rotowireTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});

	var rotogrindersBattersEntryTimesGet = $http.get('/api/baseballRotogrindersBattersTimes');

	rotogrindersBattersEntryTimesGet.success(function(response){
		console.log("Success getting Rotogrinders Batters times");
		wsa.rotogrindersBattersEntryTimes = response;
	});
	rotogrindersBattersEntryTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});

	var rotogrindersPitchersEntryTimesGet = $http.get('/api/baseballRotogrindersPitchersTimes');

	rotogrindersPitchersEntryTimesGet.success(function(response){
		console.log("Success getting Rotogrinders Pitchers times");
		wsa.rotogrindersPitchersEntryTimes = response;
	});
	rotogrindersPitchersEntryTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});
	
	var swishAnalyticsEntryTimesGet = $http.get('/api/baseballSwishAnalyticsBattersTimes');

	swishAnalyticsEntryTimesGet.success(function(response){
		console.log("Success getting Swish Analytics Batters times");
		wsa.swishAnalyticsBattersEntryTimes = response;
	});
	swishAnalyticsEntryTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});

	var swishAnalyticsPitcherEntryTimesGet = $http.get('/api/baseballSwishAnalyticsPitchersTimes');

	swishAnalyticsPitcherEntryTimesGet.success(function(response){
		console.log("Success getting Swish Analytics Pitchers times");
		wsa.swishAnalyticsPitchersEntryTimes = response;
	});
	swishAnalyticsPitcherEntryTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});

	wsa.showRotowire = true;

	wsa.rotowireHide = function()
	{
		wsa.showRotowire = false;
	};

	wsa.rotowireShow = function()
	{
		wsa.showRotowire = true;
	};

	wsa.showRotogrindersBatters = true;

	wsa.rotogrindersBattersHide = function()
	{
		wsa.showRotogrindersBatters = false;
	};

	wsa.rotogrindersBattersShow = function()
	{
		wsa.showRotogrindersBatters = true;
	};

	wsa.showRotogrindersPitchers = true;

	wsa.rotogrindersPitchersHide = function()
	{
		wsa.showRotogrindersPitchers = false;
	};

	wsa.rotogrindersPitchersShow = function()
	{
		wsa.showRotogrindersPitchers = true;
	};

	wsa.showSwishAnalyticsBatterData = true;

	wsa.swishAnalyticsBattersHide = function()
	{
		wsa.showSwishAnalyticsBatterData = false;
	};

	wsa.swishAnalyticsBattersShow = function()
	{
		wsa.showSwishAnalyticsBatterData = true;
	};
	
	wsa.showSwishAnalyticsPitcherData = true;

	wsa.swishAnalyticsPitchersHide = function()
	{
		wsa.showSwishAnalyticsPitcherData = false;
	};

	wsa.swishAnalyticsPitchersShow = function()
	{
		wsa.showSwishAnalyticsPitcherData = true;
	};

	function findRotowireId(time) {
		return time.scraped === wsa.rotowireSelectTime;
	}

	function findRotogrindersBattersId(time) {
		return time.scraped === wsa.rotogrindersBattersSelectedTime;
	}

	function findRotogrindersPitchersId(time) {
		return time.scraped === wsa.rotogrindersPitchersSelectedTime;
	}
	
	function findSwishAnalyticsBattersId(time) {
		return time.scraped === wsa.swishAnalyticsBattersSelectedTime;
	}

	function findSwishAnalyticsPitchersId(time) {
		return time.scraped === wsa.swishAnalyticsPitchersSelectedTime;
	}

	wsa.getRotowireData = function()
	{
		wsa.rotowireSelectedTimeObject = "";

		if (wsa.rotowireSelectTime != "")
			wsa.rotowireSelectedTimeObject = wsa.rotowireTimes.find(findRotowireId);

		// send to database
		var submit = $http.post('/api/baseballRotowireData/', wsa.rotowireSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.rotowireHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
	
	wsa.getRotogrindersBatterData = function()
	{
		wsa.rotogrindersSelectedTimeObject = "";

		if (wsa.rotogrindersBattersSelectedTime != "")
			wsa.rotogrindersSelectedTimeObject = wsa.rotogrindersBattersEntryTimes.find(findRotogrindersBattersId);

		// send to database
		var submit = $http.post('/api/baseballRotogrindersBatterData/', wsa.rotogrindersSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.rotogrindersBattersHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};

	wsa.getRotogrindersPitcherData = function()
	{
		wsa.rotogrindersPitchersSelectedTimeObject = "";

		if (wsa.rotogrindersPitchersSelectedTime != "")
		{
			wsa.rotogrindersPitchersSelectedTimeObject =
				wsa.rotogrindersPitchersEntryTimes.find(findRotogrindersPitchersId);
		}

		// send to database
		var submit = $http.post('/api/baseballRotogrindersPitcherData/', wsa.rotogrindersPitchersSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.rotogrindersPitchersHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};

	wsa.getSwishAnalyticsBatterData = function()
	{
		wsa.swishAnalyticsBattersSelectedTimeObject = "";
		
		if (wsa.swishAnalyticsBattersSelectedTime != "")
		{
			wsa.swishAnalyticsBattersSelectedTimeObject =
				wsa.swishAnalyticsBattersEntryTimes.find(findSwishAnalyticsBattersId);
		}
		
		// send to database
		var submit = $http.post('/api/baseballSwishAnalyticsBatterData/', wsa.swishAnalyticsBattersSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.swishAnalyticsBattersHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
	
	wsa.getSwishAnalyticsPitcherData = function()
	{
		wsa.swishAnalyticsPitchersSelectedTimeObject = "";

		if (wsa.swishAnalyticsPitchersSelectedTime != "")
		{
			wsa.swishAnalyticsPitchersSelectedTimeObject = wsa.swishAnalyticsPitchersEntryTimes
				.find(findSwishAnalyticsPitchersId);
		}
		// send to database
		var submit = $http.post('/api/baseballSwishAnalyticsPitcherData/',
			wsa.swishAnalyticsPitchersSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.swishAnalyticsPitchersHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
	
}]);


