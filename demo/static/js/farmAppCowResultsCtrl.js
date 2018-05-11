farmApp.controller("CowResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.cow_id;
    $scope.cow = null;
    console.log("Entered CowResultsController");

    $http({
      method: "GET",
      url: "/assets/api/cows/" + $scope.inputId + "/",
    }).then(function (response) {
      $scope.cow = response.data;
    });
});

