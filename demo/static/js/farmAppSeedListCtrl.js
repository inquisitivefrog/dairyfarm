farmApp.controller('SeedListController',
  function($scope, $http) {
    $scope.seeds = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered SeedListController");

    $http({
      method: 'GET',
      url: '/assets/api/seeds/',
    }).then(function (response) {
      $scope.seeds = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/seeds/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
