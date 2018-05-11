farmApp.controller("EventResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.event_id;
    $scope.event = null;
    $scope.base_url = "/assets/api/events/";
    console.log("Entered EventResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.event = response.data;
    });
});

