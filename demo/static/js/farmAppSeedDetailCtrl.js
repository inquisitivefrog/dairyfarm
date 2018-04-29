farmApp.controller("SeedDetailController",
  function($scope, $http, $routeParams) {
    $scope.seed_id = $routeParams.seed_id;
    $scope.seed = null;
    console.log("Entered SeedDetailController");

    $http({
      method: "GET",
      url: "/assets/api/seeds/" + $scope.seed_id + "/",
    }).then(function (response) {
      $scope.seed = response.data;
    });
});
