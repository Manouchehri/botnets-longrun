angular.module('marketingApp').
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
	when("/", {
		templateUrl: "static/app/components/home/homeView.html",
		controller: "HomeController",
		data: {
			requireLogin: true
		}
	}).when("/extra", {
		templateUrl: "static/app/components/extra/extraView.html",
		controller: "ExtraController",
		data: {
			requireLogin: true
		}
	}).when("/login", {
		templateUrl: "static/app/shared/login/loginView.html",
		controller: "LoginController",
		data: {
			requireLogin: false
		}
	})
	.otherwise({redirectTo: '/'});
}]);