farmApp.controller("LoginController",
    function ($scope, $rootScope, $http, $location) {
        $scope.username = null;
        $scope.password = null;
        $scope.token = null;
        console.log("Entered LoginController");

        $http({
            method: 'GET',
            url: '/ui_login/',
        }).then(function (response) {
            // hack as angular.element(document.forms).scope() fails to drill down as needed
            var html = response.data;
            $scope.token = html.split("input")[1].split(" ")[3].split("=")[1];
            console.log("token: " + $scope.token);
        });

        $scope.login = function() {
            var data = "username=" + $scope.username + "&"
                     + "password=" + $scope.password;
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: "/login/?next=/ui_logged_in/",
                data: data
            }).then(function (response) {
                if (typeof(response.data) == "string") {
                    var parser = new DOMParser();
                    var html = parser.parseFromString(response.data, 'text/html');
                    var p = html.firstChild.querySelectorAll("p");
                    if (p[0].innerHTML = "Please login to see this page.") {
                        console.log("p0: " + p[0].innerHTML);
                        $scope.error = "Username, password mismatch. Try again.";
                    }
                } else {
                    var user = response.data.user;
                    $rootScope.globals.currentUser = user;
                    console.log("Successfully logged in");
                    $location.url("/index/");
                }
            });
        };
    });
