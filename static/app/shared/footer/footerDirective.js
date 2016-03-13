var app = angular.module('marketingApp');

app.directive('marketingFooter', function() {
  return {
    restrict: 'E',
    replace: true,
    templateUrl: 'static/app/shared/footer/footerView.html'
  };
});