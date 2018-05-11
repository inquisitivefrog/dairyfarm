farmApp.controller("LogoutController",
    function ($scope, $rootScope, $location) {
        // reset login status
        $rootScope.globals = {};
        console.log("Entered LogoutController");

        $http({
            method: 'GET',
            url: '/logout/',
        }).then(function (response) {
            $scope.form = response.data;
            console.log("form: " + $scope.form);
        });
    });
