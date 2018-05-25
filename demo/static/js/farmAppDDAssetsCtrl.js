farmApp.controller("DDAssetsController",
    function($scope, $http, $routeParams, $location) {
        $scope.section = $routeParams.section;
        $scope.path = "#!" + $location.path();
        console.log("Entered DDAssetsController");

        if (typeof($scope.section) == "string") {
            $scope.url = "/static/templates/docs_dd_assets_" + $scope.section + ".html";
            console.log("loading url: " + $scope.url);
            $location.url($scope.url);
            //$http({
            //    method: 'GET',
            //    url: $scope.url,
            //}).then(function (response) {
            //    $scope.data = response.data;
            //});
        } else {
            console.log("table of contents loaded");
            console.log("full page loaded");
        }
});
