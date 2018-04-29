farmApp.controller('ExerciseListController',
  function($scope, $http) {
    $scope.exercises = {};
    $scope.next = null;
    $scope.prev = null;
    console.log("Entered ExerciseListController");

    $http({
      method: 'GET',
      url: '/assets/api/exercises/',
    }).then(function (response) {
      $scope.exercises = response.data.results;
      $scope.next = response.data.next;
      console.log("Next link: " + $scope.next);
      // http://localhost:8000/assets/api/exercises/?limit=10&offset=10
      $scope.prev = response.data.prev;
    });
});
