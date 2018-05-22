farmApp.controller("LoginController",
    function ($scope, $rootScope, $http, $location) {
        $scope.username = null;
        $scope.password = null;
        console.log("Entered LoginController");

        $http({
            method: 'GET',
            url: '/ui_login/',
        }).then(function (response) {
            // hack as angular.element(document.forms).scope() fails to drill down as needed
            var html = response.data;
            $rootScope.globals["token"] = html.split("input")[1].split(" ")[3].split("=")[1];
            $rootScope.globals["limit"] = 10;
        });

        $scope.globals = $rootScope.globals;
        $scope.login = function() {
            var data = "username=" + $scope.username + "&"
                     + "password=" + $scope.password;
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
                    $rootScope.globals["currentUser"] = user;
                    $rootScope.globals["login"] = currentDateTime();
                    console.log("globals set: " + Object.getOwnPropertyNames($rootScope.globals));
                    var greeting = $rootScope.globals.currentUser.username
                                 + " successfully logged in at "
                                 + $rootScope.globals.login;
                    console.log(greeting);
                    $location.url("/cache/");
                }
            });
        };
    });
