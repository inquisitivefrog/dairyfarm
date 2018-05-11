farmApp.controller('MonthlySummaryController',
  function($scope, $http, $routeParams) {
    $scope.rows = [];
    $scope.year = $routeParams.year;
    $scope.month = $routeParams.month;
    console.log('Entered MonthlySummaryController');

    if ($scope.month) {
        $http({
            method: 'GET',
            url: "/summary/api/monthly/" + $scope.year + "/" + $scope.month + "/",
        }).then(function (response) {
            $scope.row = response.data[0];
            $scope.month = $scope.row.month;
        });

    } else {
        $http({
            method: 'GET',
            url: "/summary/api/monthly/" + $scope.year + "/",
        }).then(function (response) {
            $scope.rows = response.data;
            $scope.year = response.data[0].year;
        });
    }

    
});
