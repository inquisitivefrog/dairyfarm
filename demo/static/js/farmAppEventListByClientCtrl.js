farmApp.controller('EventListByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.record_header = "Record an Event for "
                             + $rootScope.globals.currentUser.client.name;
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.events = {};
        $scope.total = null;
        $scope.event = null;
        $scope.base_url = "/assets/api/events/";
        $scope.client_url = $scope.base_url + "client/" + $scope.client + "/";
        $scope.url = null;
        $scope.record = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered EventListByClientController");

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
            $scope.events = response.data.results;
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
                     + "event_time=" + convertDateTime($scope.inputTime) + "&"
                     + "cow=" + $scope.selectedCow.rfid + "&"
                     + "action=" + $scope.selectedAction.name;
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: $scope.base_url,
                data: data
            }).then(function (response) {
                $scope.event = response.data;
                console.log("Created Event ID: " + $scope.event.id);
                $location.url($scope.base_url + $scope.event.id + "/results/");
            });
        };
});
