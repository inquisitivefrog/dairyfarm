farmApp.controller('MonthlySummaryController',
  function($scope, $http, $routeParams) {
    $scope.rows = [];
    $scope.year = $routeParams.year;
    console.log('Entered MonthlySummaryController');

    $http({
          method: 'GET',
          url: "/summary/api/monthly/" + $scope.year + "/",
    }).then(function (response) {
          $scope.rows = response.data;
          $scope.year = response.data[0].year;
    });
});
