var app = angular.module("marketingApp", ['ngRoute', 'ngCookies']);

app.constant('GLOBAL_CONFIG', {
  // if we want any variable put them here
});

app.run(function ($rootScope, $location) {

	$rootScope.$on("$routeChangeStart", function (event, toState, toParams) {
		var requireLogin = toState.data.requireLogin;
		if($rootScope.globals) {
			if (requireLogin && typeof $rootScope.globals.currentUser === 'undefined') {
	      		$location.path( "/login");
	    	}
    	} else if(requireLogin){
    		$location.path( "/login");
    	} 
	});

});

app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
  // initial config here
  $routeProvider.otherwise({redirectTo:'/home'});
}]);
