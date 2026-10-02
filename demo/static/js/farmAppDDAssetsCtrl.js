farmApp.controller("DDAssetsController",
    function($scope, $location) {
        $scope.path = "#!" + $location.path();
});
