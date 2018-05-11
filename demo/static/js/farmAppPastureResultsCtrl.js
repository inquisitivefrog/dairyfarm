farmApp.controller("PastureResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.pasture_id;
    $scope.pasture = null;
    $scope.base_url = "/assets/api/pastures/";
    console.log("Entered PastureResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.pasture = response.data;
    });
});

