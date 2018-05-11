farmApp.controller("HealthRecordResultsController",
  function($scope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.hr_id;
    $scope.hr = null;
    $scope.base_url = "/assets/api/healthrecords/";
    console.log("Entered HealthRecordResultsController");

    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.hr = response.data;
    });
});

