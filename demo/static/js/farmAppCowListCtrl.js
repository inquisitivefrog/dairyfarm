farmApp.controller('CowListController',
  function($scope, $http) {
    $scope.herd = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered CowListController");

    $http({
      method: 'GET',
      url: '/assets/api/cows/',
    }).then(function (response) {
      $scope.herd = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/cows/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
