farmApp.controller("LoginController",
    function ($scope, $rootScope, $http, $location) {
        $scope.username = null;
        $scope.password = null;
        $scope.token = null;
        console.log("Entered LoginController");

        $http({
            method: 'GET',
            url: '/login/',
        }).then(function (response) {
            // hack as angular.element(document.forms).scope() fails to drill down as needed
            var html = response.data;
            $scope.token = html.split("form")[1].split("input")[1].split(" ")[3].split("=")[1];
            console.log("token: " + $scope.token);
        });

        $scope.login = function () {
            var data = "username=" + $scope.username + "&"
                     + "password=" + $scope.password;
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: "/login/",
                data: data
            }).then(function (response) {
                $rootScope.globals.currentUser = response.data;
                console.log("current user: " + $rootScope.globals.currentUser);
                $location.url("#/");
            });
        };
    });
