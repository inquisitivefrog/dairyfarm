farmApp.controller('ReloadCacheController',
  function($scope, $rootScope, $http, $routeParams, $location, $q) {
      $scope.quiet = $routeParams.quiet;
      $scope.globals = $rootScope.globals;
      if ($scope.quiet == null) {
          $scope.debug = false;
      } else {
          $scope.debug = true;
      }
      console.log('Entered ReloadCacheController');

      var requests = [];
      function load(url, key) {
          requests.push($http({
              method: 'GET',
              url: url,
          }).then(function (response) {
              $rootScope.globals[key] = response.data.results;
          }));
      }

      load('/assets/api/breeds/?limit=20', 'breeds');
      load('/assets/api/colors/?limit=20', 'colors');
      load('/assets/api/ages/', 'ages');
      load('/assets/api/actions/?limit=50', 'actions');
      load('/assets/api/seasons/?limit=20', 'seasons');
      load('/assets/api/cereals/?limit=20', 'cereals');
      load('/assets/api/grasses/?limit=20', 'grasses');
      load('/assets/api/legumes/?limit=20', 'legumes');
      load('/assets/api/statuses/?limit=20', 'statuses');
      load('/assets/api/illnesses/?limit=20', 'illnesses');
      load('/assets/api/injuries/?limit=20', 'injuries');
      load('/assets/api/treatments/?limit=20', 'treatments');
      load('/assets/api/vaccines/?limit=20', 'vaccines');
      load(
          "/assets/api/cows/client/"
              + $rootScope.globals.currentUser.client.id + "/?limit=50",
          'cows'
      );
      load(
          "/assets/api/pastures/client/"
              + $rootScope.globals.currentUser.client.id + "/",
          'pastures'
      );

      $q.all(requests).then(function () {
          console.log(
              "globals set: "
                  + Object.getOwnPropertyNames($rootScope.globals));
          if ($scope.quiet == null || $scope.quiet === 'switch') {
              $location.url("/home/");
          }
      });
});
