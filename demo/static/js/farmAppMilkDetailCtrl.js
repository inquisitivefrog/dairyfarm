farmApp.controller("MilkDetailController",
  function($scope, $http, $routeParams) {
    $scope.milk_id = $routeParams.milk_id;
    $scope.milk = null;
    console.log("Entered MilkDetailController");

    $http({
      method: "GET",
      url: "/assets/api/milk/" + $scope.milk_id + "/",
    }).then(function (response) {
      $scope.milk = response.data;
    });
});
