farmApp.controller("ExerciseDetailController",
  function($scope, $http, $routeParams) {
    $scope.exercise_id = $routeParams.exercise_id;
    $scope.exercise = null;
    console.log("Entered ExerciseDetailController");

    $http({
      method: "GET",
      url: "/assets/api/exercises/" + $scope.exercise_id + "/",
    }).then(function (response) {
      $scope.exercise = response.data;
    });
});
