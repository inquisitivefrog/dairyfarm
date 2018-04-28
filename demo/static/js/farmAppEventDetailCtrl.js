farmApp.controller("EventDetailController",
  function($scope, $http, $routeParams) {
    $scope.event_id = $routeParams.event_id;
    $scope.event = null;
    console.log("Entered EventDetailController");

    $http({
      method: "GET",
      url: "/assets/api/events/" + $scope.event_id + "/",
    }).then(function (response) {
      $scope.event = response.data;
    });
});
