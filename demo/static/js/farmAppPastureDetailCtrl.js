farmApp.controller("PastureDetailController",
  function($scope, $http, $routeParams) {
    $scope.pasture_id = $routeParams.pasture_id;
    $scope.pasture = null;
    console.log("Entered PastureDetailController");

    $http({
      method: "GET",
      url: "/assets/api/pastures/" + $scope.pasture_id + "/",
    }).then(function (response) {
      $scope.pasture = response.data;
    });
});
