var app = angular.module("marketingApp", ['ngRoute']);

app.constant('GLOBAL_CONFIG', {
  // if we want any variable put them here
});

app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
  // initial config here
  $locationProvider.html5Mode(true);
  $routeProvider.otherwise({redirectTo:'/home'});
}]);