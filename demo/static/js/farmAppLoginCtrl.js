farmApp.controller("LoginController",
    function ($scope, $rootScope, $http, $httpParamSerializer, $location) {
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
                data: $httpParamSerializer({
                    username: $scope.username,
                    password: $scope.password,
                    csrfmiddlewaretoken: $rootScope.globals.token,
                    next: "/ui_logged_in/"
                })
            }).then(function (response) {
                if (typeof(response.data) == "string") {
                    $scope.error =
                        "Login failed. Check the username and password and try again.";
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
