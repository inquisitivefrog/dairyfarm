farmApp.controller("CowDetailController",
  function($scope, $http, $routeParams) {
    $scope.cow_id = $routeParams.cow_id;
    $scope.cow = null;
    console.log("Entered CowDetailController");

    $http({
      method: "GET",
      url: "/assets/api/cows/" + $scope.cow_id + "/",
    }).then(function (response) {
      $scope.cow = response.data;
    });
});
