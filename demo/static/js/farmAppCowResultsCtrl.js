farmApp.controller("CowResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.cow_id;
    $scope.base_url = "/assets/api/cows/";
    $scope.cow = null;
    console.log("Entered CowResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.cow = response.data;
    });
});
