farmApp.controller('EventListController',
  function($scope, $http) {
    $scope.events = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered EventListController");

    $http({
      method: 'GET',
      url: '/assets/api/events/',
    }).then(function (response) {
      $scope.events = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/events/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
