farmApp.controller('MonthlySummaryByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.year = $routeParams.year;
        $scope.month = $routeParams.month;
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.report_header = "Monthly Reports for " + $scope.year;
        $scope.base_url = "/summary/api/monthly/client/" 
                        + $scope.client + "/";

        $scope.rows = [];
        console.log('Entered MonthlySummaryByClientController');

        $scope.globals = $rootScope.globals;
        console.log("globals set: " + Object.getOwnPropertyNames($scope.globals));

        if ($scope.month) {
            $scope.client_url = $scope.base_url 
                              + "year/" + $scope.year 
                              + "/month/" + $scope.month + "/";
            $http({
                method: 'GET',
                url: $scope.client_url,
            }).then(function (response) {
                $scope.row = response.data[0];
                $scope.month = $scope.row.month;
            });

        } else {
            $scope.client_url = $scope.base_url 
                              + "year/" + $scope.year + "/";
            $http({
                method: 'GET',
                url: $scope.client_url,
            }).then(function (response) {
                $scope.rows = response.data;
                $scope.year = response.data[0].year;
            });
        }
});
