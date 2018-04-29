farmApp.controller('MilkListController',
  function($scope, $http) {
    $scope.milk = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered MilkListController");

    $http({
      method: 'GET',
      url: '/assets/api/milk/',
    }).then(function (response) {
      $scope.milk = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/milk/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
