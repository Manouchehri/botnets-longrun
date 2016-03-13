var app = angular.module('marketingApp');

app.directive('marketingMenu', function() {
  return {
    restrict: 'E',
    replace: true,
    templateUrl: 'app/shared/menu/menuView.html'
  };
});