farmApp.controller("LoginController",
    function ($scope, $rootScope, $http, $httpParamSerializer, $location) {
        $scope.username = null;
        $scope.password = null;
        $scope.loginReady = false;
        console.log("Entered LoginController");

        $http.get('/ui_login/').then(function () {
            $scope.loginReady = true;
            $rootScope.globals["limit"] = 10;
        }, function () {
            $scope.error = "Unable to initialize login. Please reload the page.";
        });

        $scope.globals = $rootScope.globals;
        $scope.login = function() {
            if (!$scope.loginReady) {
                return;
            }

            $scope.error = null;
            $http({
                method: 'POST',
                url: "/login/?next=/ui_logged_in/",
                data: $httpParamSerializer({
                    username: $scope.username,
                    password: $scope.password,
                    next: "/ui_logged_in/"
                })
            }).then(function (response) {
                if (typeof(response.data) == "string") {
                    $scope.error =
                        "Login failed. Check the username and password and try again.";
                    return;
                }

                var user = response.data.user;
                $rootScope.globals["currentUser"] = user;
                $rootScope.globals["login"] = currentDateTime();
                console.log("globals set: " + Object.getOwnPropertyNames($rootScope.globals));
                var greeting = $rootScope.globals.currentUser.username
                             + " successfully logged in at "
                             + $rootScope.globals.login;
                console.log(greeting);
                $location.url("/cache/");
            }, function () {
                $scope.error =
                    "Login request failed. Please reload the page and try again.";
            });
        };
    });
