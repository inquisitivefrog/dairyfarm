farmApp.controller("LogoutController",
    function ($scope, $http, $rootScope, $location) {
        // reset login status
        $scope.logout = null;
        $scope.username = $rootScope.globals.currentUser.username;
        $scope.logout = currentDateTime();
        console.log("Entered LogoutController");

        $http({
            method: 'POST',
            url: '/ui_logout/',
        }).then(function (response) {
            $rootScope.globals = {};
            console.log("globals unset");
            $location.path('/login/');
        });
    });
