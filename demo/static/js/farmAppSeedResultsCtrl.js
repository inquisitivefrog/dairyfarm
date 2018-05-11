farmApp.controller("SeedResultsController",
  function($scope, $http, $routeParams, $location) {
      $scope.inputId = $routeParams.seed_id;
      $scope.seed = null;
      $scope.base_url = "/assets/api/seeds/";
      console.log("Entered SeedResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.seed = response.data;
    });
});
