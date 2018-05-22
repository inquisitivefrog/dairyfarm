farmApp.controller('AnnualSummaryByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.year = $routeParams.year;
        $scope.report_header = $rootScope.globals.currentUser.client.name 
                             + " Annual Reports";
        $scope.rows = [];
        $scope.total = null;
        $scope.base_url = "/summary/api/annual/client/" 
                        + $scope.client + "/";
        if ($scope.year) {
            $scope.client_url = $scope.base_url 
                              + "year/" + $scope.year + "/";
        } else {
            $scope.client_url = $scope.base_url; 
        }
        console.log("Entered AnnualSummaryByClientController");
        console.log("url: " + $scope.client_url);

        $scope.globals = $rootScope.globals;
        console.log("globals set: " + Object.getOwnPropertyNames($scope.globals));

        $http({
            method: "GET",
            url: $scope.client_url,
        }).then(function (response) {
            $scope.response = response;
            $scope.rows = response.data;
            $scope.total = $scope.rows.length;
        });
});
