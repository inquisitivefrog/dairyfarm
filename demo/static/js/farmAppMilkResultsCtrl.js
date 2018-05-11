farmApp.controller("MilkResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.milk_id;
    $scope.milk = null;
    $scope.base_url = "/assets/api/milk/";
    console.log("Entered MilkResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.milk = response.data;
    });
});

