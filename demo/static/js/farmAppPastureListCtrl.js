farmApp.controller('PastureListController',
  function($scope, $http) {
    $scope.pastures = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered PastureListController");

    $http({
      method: 'GET',
      url: '/assets/api/pastures/',
    }).then(function (response) {
      $scope.pastures = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/pastures/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
