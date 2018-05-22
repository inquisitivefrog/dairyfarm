farmApp.controller("HealthRecordResultsController",
  function($scope, $rootScope, $http, $routeParams, $location) {
    $scope.inputId = $routeParams.hr_id;
    $scope.hr = null;
    $scope.inspect_header = "Cow inspected for "
                          + $rootScope.globals.currentUser.client.name;
    $scope.base_url = "/assets/api/healthrecords/";
    console.log("Entered HealthRecordResultsController");

    $scope.globals = $rootScope.globals;
    $http({
      method: "GET",
      url: $scope.base_url + $scope.inputId + "/",
    }).then(function (response) {
      $scope.hr = response.data;
    });
});

