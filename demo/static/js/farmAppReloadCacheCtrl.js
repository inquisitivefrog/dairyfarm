farmApp.controller('ReloadCacheController',
  function($scope, $rootScope, $http, $routeParams, $location) {
      $scope.quiet = $routeParams.quiet;
      $scope.globals = null;
      if ($scope.quiet == null) {
          $scope.debug = false;
      } else {
          $scope.debug = true;
      }
      console.log('Entered ReloadCacheController');

    $http({
        method: 'GET',
        url: '/assets/api/breeds/?limit=20',
    }).then(function (response) {
        $rootScope.globals.breeds = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/colors/?limit=20',
    }).then(function (response) {
        $rootScope.globals.colors = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/ages/',
    }).then(function (response) {
        $rootScope.globals.ages = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/actions/?limit=50',
    }).then(function (response) {
        $rootScope.globals.actions = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/seasons/?limit=20',
    }).then(function (response) {
        $rootScope.globals.seasons = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/cereals/?limit=20',
    }).then(function (response) {
        $rootScope.globals.cereals = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/grasses/?limit=20',
    }).then(function (response) {
        $rootScope.globals.grasses = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/legumes/?limit=20',
    }).then(function (response) {
        $rootScope.globals.legumes = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/statuses/?limit=20',
    }).then(function (response) {
        $rootScope.globals.statuses = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/illnesses/?limit=20',
    }).then(function (response) {
        $rootScope.globals.illnesses = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/injuries/?limit=20',
    }).then(function (response) {
        $rootScope.globals.injuries = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/treatments/?limit=20',
    }).then(function (response) {
        $rootScope.globals.treatments = response.data.results;
    });

    $http({
        method: 'GET',
        url: '/assets/api/vaccines/?limit=20',
    }).then(function (response) {
        $rootScope.globals.vaccines = response.data.results;
    });

    $http({
        method: 'GET',
        url: "/assets/api/cows/client/"
             + $rootScope.globals.currentUser.client.id + "/?limit=50",
    }).then(function (response) {
        $rootScope.globals.cows = response.data.results;
    });

    $http({
        method: 'GET',
        url: "/assets/api/pastures/client/"
             + $rootScope.globals.currentUser.client.id + "/",
    }).then(function (response) {
        $rootScope.globals.pastures = response.data.results;
    });

    $scope.globals = $rootScope.globals;
    console.log("globals set: " + Object.getOwnPropertyNames($rootScope.globals));
    console.log("currentUser: " + Object.getOwnPropertyNames($rootScope.globals.currentUser));
    if ($scope.quiet == null) {
        $location.url("/home/");
    }
});
