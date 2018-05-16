farmApp.controller("AnnualSummaryController",
  function($scope, $http, $rootScope) {
    $scope.rows = [];
    $scope.response = null;
    $scope.globals = $rootScope.globals;
    console.log("Entered AnnualSummaryController");
    console.log("globals: " + Object.getOwnPropertyNames($scope.globals));

    $http({
          method: "GET",
          url: "/summary/api/annual/",
    }).then(function (response) {
          $scope.response = response;
          $scope.rows = response.data;
    });
});
