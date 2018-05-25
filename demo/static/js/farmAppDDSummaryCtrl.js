farmApp.controller('DDSummaryController',
    function($scope, $http, $routeParams, $location) {
        $scope.section = $routeParams.section;
        $scope.path = "#!" + $location.path();
        console.log('Entered DDSummaryController');

        if (typeof($scope.section) == "string") {
            $scope.url = "/static/templates/docs_dd_summary_" + $scope.section + ".html";
            $http({
                method: 'GET',
                url: $scope.url,
            }).then(function (response) {
                $scope.data = response.data;
            });
            console.log("table of contents loaded");
            console.log("calling url: " + $scope.url);
        } else {
            console.log("full page loaded");
        }
});
