farmApp.controller('MilkListController',
  function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.milk = null;
        $scope.total = null;
        $scope.m = null;
        $scope.base_url = "/assets/api/milk/";
        $scope.url = null;
        $scope.record = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered MilkListController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.base_url + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.base_url;
        }
        $http({
            method: 'GET',
            url: $scope.url,
        }).then(function (response) {
            $scope.milk = response.data.results;
            $scope.total = response.data.count;
            if (($scope.offset == null) && ($scope.limit == null)) {
                // set beginning
                $scope.offset = $rootScope.globals.limit;
                $scope.limit = $rootScope.globals.limit;
                $scope.next = "#" + $scope.base_url + "limit/" + $scope.limit + "/offset/" + $scope.offset + "/";
                $scope.prev = null;
            } else {
                offset = parseInt($scope.offset) + parseInt($scope.limit);
                if (offset < parseInt($scope.total)) {
                    $scope.next = "#" + $scope.base_url + "limit/" + $scope.limit + "/offset/" + offset + "/";
                } else {
                    $scope.next = null;
                }
                offset = parseInt($scope.offset) - parseInt($scope.limit);
                if (offset >= $scope.limit) {
                    $scope.prev = "#" + $scope.base_url + "limit/" + $scope.limit + "/offset/" + offset + "/";
                } else {
                    $scope.prev = "#" + $scope.base_url;
                }
            }
        });

        $scope.clients = $rootScope.globals.clients;
        $scope.users = $rootScope.globals.users;
        $scope.cows = $rootScope.globals.cows;

        $scope.record = function () {
            var data = "client=" + $scope.selectedClient.name + "&"
                     + "recorded_by=" + $scope.selectedRecorder.username + "&"
                     + "milking_time=" + convertDateTime($scope.inputTime) + "&"
                     + "cow=" + $scope.selectedCow.rfid + "&"
                     + "gallons=" + $scope.inputGallons;
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: $scope.base_url,
                data: data
            }).then(function (response) {
                $scope.m = response.data;
                console.log("Created Milk ID: " + $scope.m.id);
                $location.url($scope.base_url + $scope.m.id + "/results/");
            });
        };
});
