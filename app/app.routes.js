angular.module('marketingApp').
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
	when("/", {
		templateUrl: "app/components/home/homeView.html",
		controller: "HomeController"
	}).when("/extra", {
		templateUrl: "app/components/extra/extraView.html",
		controller: "ExtraController"
	})
	.otherwise({redirectTo: '/'});
}]);