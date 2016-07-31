var app = angular.module('WSAData', ['ngSanitize']);

app.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
}]);



app.controller("mainController", ['$scope', '$http', '$location', '$window', function($scope, $http, $location) {
	var wsa = this;

	wsa.validate = function(inUsername, inPassword)
	{
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

	wsa.signUp = function(inFirstName, inLastName, inEmail, inPassword, inConfirmPassword)
	{
		var data = {
			password: inPassword,
			confirmPassword: inConfirmPassword,
			firstName: inFirstName,
			lastName: inLastName,
			email: inEmail
		};

		var submit = $http.post('/api/signUp/', data);

		submit.success(function(response){
			console.log("Success: " + response.toString());
			window.location.replace('/data/')
		});

		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};
}]);

app.controller("homeController", ['$scope', '$http', '$window', function($scope, $http) {
	var wsa = this;

	var userInformation = $http.get('/api/getUserData/');

	userInformation.success(function(response) {
		console.log("Success getting User Data");
		wsa.userData = response;
	});

	userInformation.error(function(response) {
		console.log("Error " + response.toString());
	});

	wsa.logout = function() {
		var logoutRequest = $http.post('/api/logoutUser/');

		logoutRequest.success(function(response) {
			console.log("Success logging out");
			window.location.replace('/')
		});

		logoutRequest.error(function(response) {
			console.log("Error logging out. You are trapped! " + response.toString());
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

	var pitcherLeftHandSplitsEntryTimesGet = $http.get('/api/baseballPitcherLeftHandSplitsTimes');

	pitcherLeftHandSplitsEntryTimesGet.success(function(response){
		console.log("Success getting Left Hand Pitcher Splits times");
		wsa.pitcherLeftHandSplitsEntryTimes = response;
	});
	pitcherLeftHandSplitsEntryTimesGet.error(function(response){
		console.log("Error: ", + response.toString())
	});

	var pitcherRightHandSplitsEntryTimesGet = $http.get('/api/baseballPitcherRightHandSplitsTimes');

	pitcherRightHandSplitsEntryTimesGet.success(function(response){
		console.log("Success getting Right Hand Pitcher Splits times");
		wsa.pitcherRightHandSplitsEntryTimes = response;
	});
	pitcherRightHandSplitsEntryTimesGet.error(function(response){
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

	wsa.showPitcherRightHandSplits = true;

	wsa.pitcherRightHandSplitsHide = function()
	{
		wsa.showPitcherRightHandSplits = false;
	};

	wsa.pitcherRightHandSplitsShow = function()
	{
		wsa.showPitcherRightHandSplits = true;
	};

	wsa.showPitcherLeftHandSplits = true;

	wsa.pitcherLeftHandSplitsHide = function()
	{
		wsa.showPitcherLeftHandSplits = false;
	};

	wsa.pitcherLeftHandSplitsShow = function()
	{
		wsa.showPitcherLeftHandSplits = true;
	};

	wsa.showLeftHandedBatterSplits = true;

	wsa.leftHandedBatterSplitsHide = function()
	{
		wsa.showLeftHandedBatterSplits = false;
	};

	wsa.leftHandedBatterSplitsShow = function()
	{
		wsa.showLeftHandedBatterSplits = true;
	};

	wsa.showRightHandedBatterSplits = true;

	wsa.rightHandedBatterSplitsHide = function()
	{
		wsa.showRightHandedBatterSplits = false;
	};

	wsa.rightHandedBatterSplitsShow = function()
	{
		wsa.showRightHandedBatterSplits = true;
	};

	wsa.showRightHandedAdvancedBatterSplits = true;

	wsa.rightHandedAdvBatterSplitsHide = function()
	{
		wsa.showRightHandedAdvancedBatterSplits = false;
	};

	wsa.rightHandedAdvBatterSplitsShow = function()
	{
		wsa.showRightHandedAdvancedBatterSplits = true;
	};

	wsa.showLeftHandedAdvancedBatterSplits = true;

	wsa.leftHandedAdvBatterSplitsHide = function()
	{
		wsa.showLeftHandedAdvancedBatterSplits = false;
	};

	wsa.leftHandedAdvBatterSplitsShow = function()
	{
		wsa.showLeftHandedAdvancedBatterSplits = true;
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

	function findRightPitcherSplitsId(time) {
		return time.scraped === wsa.rightHandedPitcherSplitsSelectedTime;
	}

	function findLeftPitcherSplitsId(time) {
		return time.scraped === wsa.leftHandedPitcherSplitsSelectedTime;
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

	wsa.getPitcherRightHandSplitsData = function()
	{
		wsa.rightHandedPitcherSplitsSelectedTimeObject = "";

		if (wsa.rightHandedPitcherSplitsSelectedTime != "")
		{
			wsa.rightHandedPitcherSplitsSelectedTimeObject = wsa.pitcherRightHandSplitsEntryTimes
				.find(findRightPitcherSplitsId);
		}
		// send to database
		var submit = $http.post('/api/baseballRotogrindersRightHandedPitcherSplits/',
			wsa.rightHandedPitcherSplitsSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.pitcherRightHandSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};

	wsa.getPitcherLeftHandSplitsData = function()
	{
		wsa.leftHandedPitcherSplitsSelectedTimeObject = "";

		if (wsa.leftHandedPitcherSplitsSelectedTime != "")
		{
			wsa.leftHandedPitcherSplitsSelectedTimeObject = wsa.pitcherLeftHandSplitsEntryTimes
				.find(findLeftPitcherSplitsId);
		}
		// send to database
		var submit = $http.post('/api/baseballRotogrindersLeftHandedPitcherSplits/',
			wsa.leftHandedPitcherSplitsSelectedTimeObject);

		submit.success(function(response){
			console.log("Success");
			wsa.pitcherLeftHandSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	};

	wsa.getLeftHandedBatterSplitsData = function()
	{
		var submit = $http.post('/api/baseballRotogrindersLeftHandedBatterSplits/', '');

		submit.success(function(response){
			console.log("Success");
			wsa.batterLeftHandedSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	}

	wsa.getRightHandedBatterSplitsData = function()
	{
		var submit = $http.post('/api/baseballRotogrindersRightHandedBatterSplits/', '');

		submit.success(function(response){
			console.log("Success");
			wsa.batterRightHandedSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	}

	wsa.getLeftHandedAdvancedBatterSplitsData = function()
	{
		var submit = $http.post('/api/baseballRotogrindersLeftHandedAdvancedBatterSplits/', '');

		submit.success(function(response){
			console.log("Success");
			wsa.batterLeftHandedAdvancedSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	}

	wsa.getRightHandedAdvancedBatterSplitsData = function()
	{
		var submit = $http.post('/api/baseballRotogrindersRightHandedAdvancedBatterSplits/', '');

		submit.success(function(response){
			console.log("Success");
			wsa.batterRightHandedAdvancedSplitsData = response.toString();
		});
		submit.error(function(response){
			console.log("Error: ", + response.toString())
		});
	}
	
}]);

/*
app.controller("baseballUploadController", ['$scope', '$http', '$location', '$window', function($scope, $http, $location) {
	var wsa = this;

	wsa.uploadSaberSimBatters = function() {
		var file = document.getElementById('saberSimBatterFile').files[0];
		var r = new FileReader();

		r.onloadend = function(e) {
			var data = e.target.result;

			var submit = $http.post('/api/uploadSaberSimBatters/', file, data);

			submit.success(function(response){
				console.log("Success");
			});
			submit.error(function(response){
				console.log("Error: ", + response.toString())
			});
		};

		r.readAsBinaryString(file);
	};
}]);
*/
