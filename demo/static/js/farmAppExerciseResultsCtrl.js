farmApp.controller("ExerciseResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.exercise_id;
    $scope.exercise = null;
    $scope.base_url = "/assets/api/exercises/";
    console.log("Entered ExerciseResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.exercise = response.data;
    });
});

