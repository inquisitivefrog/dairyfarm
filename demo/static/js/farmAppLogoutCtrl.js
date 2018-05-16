farmApp.controller("LogoutController",
    function ($scope, $http, $rootScope, $location) {
        // reset login status
        $rootScope.globals = {};
        console.log("Entered LogoutController");

        $http({
            method: 'GET',
            url: '/ui_logout/',
        }).then(function (response) {
            console.log("globals unset");
        });
    });
