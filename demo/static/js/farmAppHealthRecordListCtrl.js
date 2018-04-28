farmApp.controller('HealthRecordListController',
  function($scope, $http) {
    $scope.hrs = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered HealthRecordListController");

    $http({
      method: 'GET',
      url: '/assets/api/healthrecords/',
    }).then(function (response) {
      $scope.hrs = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/healthrecords/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
