var farmApp = angular.module('farmApp', ['ngRoute']).config(
  function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    var ctype = 'application/x-www-form-urlencoded;charset=utf-8'; 
    $httpProvider.defaults.headers.post['Content-Type'] = ctype;
});

farmApp.controller('AssetController',
  function AssetController($scope, $http) {
    $scope.herd = null;

    $http({
      method: 'GET',
      url: '/assets/api/cows/',
    }).then(function (response) {
      $scope.herd = response.data.count();
      console.log($scope.herd);
    });
});

farmApp.controller('HerdController',
  function HerdController($scope, $http, $routeParams, $location) {
    $scope.cow_id = $routeParams.cow_id;
    $scope.cow = null;
    $scope.selected_choice = {
      choice: 0
    };

    $http({
      method: 'GET',
      url: '/assets/api/cows/'+$scope.cow_id}).then(function (response) {
      $scope.question = response.data;
    })

    $scope.purchaseCow = function () {
      $http({
        method: 'POST',
        url: '/assets/api/cows/',
        data: "choice="+$scope.selected_choice.choice
      }).then(function (response) {
        $location.url('/assets/api/cows/'+$scope.cow_id+'/results/');
      })
    }
  })

angular.
  module('farmApp').
  config(['$routeProvider',
    function config($routeProvider) {

      $routeProvider.
        when('/', {
          templateUrl: '/static/templates/index.html',
          controller: 'AssetController'
        }).
        when('/assets/api/cows/:cow_id/results/', {
          templateUrl: '/static/templates/herd_results.html',
          controller: 'HerdController'
        }).
        when('/assets/api/cows/:cow_id/', {
          templateUrl: '/static/templates/herd_detail.html',
          controller: 'HerdController'
        }).
        otherwise('/');
    }
  ]);
