farmApp.controller('MilkListByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.purchase_header = "Milk a Cow for "
                               + $rootScope.globals.currentUser.client.name;
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.milk = {};
        $scope.total = null;
        $scope.m = null;
        $scope.base_url = "/assets/api/milk/";
        $scope.client_url = $scope.base_url + "client/" + $scope.client + "/";
        $scope.url = null;
        $scope.record = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered MilkListByClientController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.client_url
                       + "?limit=" + $scope.limit 
                       + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.client_url;
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
                if ($scope.total > $scope.limit) {
                    $scope.next = "#!" + $scope.client_url
                                + "limit/" + $scope.limit
                                + "/offset/" + $scope.offset + "/";
                } else {
                    delete $scope.next;
                }
                delete $scope.prev;
            } else {
                offset = parseInt($scope.offset) + parseInt($scope.limit);
                if (offset < parseInt($scope.total)) {
                    $scope.next = "#!" + $scope.client_url
                                + "limit/" + $scope.limit 
                                + "/offset/" + offset + "/";
                } else {
                    delete $scope.next;
                }
                offset = parseInt($scope.offset) - parseInt($scope.limit);
                if (offset >= $scope.limit) {
                    $scope.prev = "#!" + $scope.client_url
                                + "limit/" + $scope.limit 
                                + "/offset/" + offset + "/";
                } else {
                    $scope.prev = "#!" + $scope.client_url; 
                }
                console.log("next: " + $scope.next);
                console.log("prev: " + $scope.prev);
            }
        });

        $scope.globals = $rootScope.globals; 
        $scope.record = function () {
            var data = "client=" + $scope.globals.currentUser.client.name + "&"
                     + "recorded_by=" + $scope.globals.currentUser.username + "&"
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
