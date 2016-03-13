var app = angular.module('marketingApp');

app.directive('marketingMenu', function() {
  return {
    restrict: 'E',
    replace: true,
    templateUrl: 'static/app/shared/menu/menuView.html'
  };
});