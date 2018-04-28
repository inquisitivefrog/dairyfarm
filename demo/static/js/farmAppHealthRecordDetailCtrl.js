farmApp.controller("HealthRecordDetailController",
  function($scope, $http, $routeParams) {
    $scope.hr_id = $routeParams.hr_id;
    $scope.hr = null;
    console.log("Entered HealthRecordDetailController");

    $http({
      method: "GET",
      url: "/assets/api/healthrecords/" + $scope.hr_id + "/",
    }).then(function (response) {
      $scope.hr = response.data;
    });
});
