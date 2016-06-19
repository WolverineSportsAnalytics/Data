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

	var rotowireTimesGet = $http.get('/api/baseballRotowireTimes/');

	rotowireTimesGet.success(function(response){
		console.log("Success getting times");
		wsa.rotowireTimes = response;
	});
	rotowireTimesGet.error(function(response){
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

	function findId(times) {
		return times.scraped === wsa.rotowireSelectTime;
	}

	wsa.getRotowireData = function()
	{
		wsa.rotowireSelectedTimeObject = ""

		if (wsa.rotowireSelectTime != "")
			wsa.rotowireSelectedTimeObject = wsa.rotowireTimes.find(findId);

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
		// send to database
		var submit = $http.get('/api/baseballRotogrindersBatterData/');

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
		// send to database
		var submit = $http.get('/api/baseballRotogrindersPitcherData/');

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
		// send to database
		var submit = $http.get('/api/baseballSwishAnalyticsBatterData/');

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
		// send to database
		var submit = $http.get('/api/baseballSwishAnalyticsPitcherData/');

		submit.success(function(response){
			console.log("Success");
			wsa.swishAnalyticsPitchersHTML = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
	
}]);


