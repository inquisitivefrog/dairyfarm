farmApp.controller("LogoutController",
    function ($scope, $http, $rootScope, $cookies) {
        // reset login status
        $scope.logout = null;
        $scope.username = $rootScope.globals.currentUser.username;
        $scope.logout = currentDateTime();
        console.log("Entered LogoutController");

        $http({
            method: 'GET',
            url: '/ui_logout/',
        }).then(function (response) {
            $rootScope.globals = $cookies.get('globals') || {};
            console.log("globals unset");
        });
    });
