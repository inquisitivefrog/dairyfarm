farmApp.controller('HealthRecordListByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.inspect_header = "Inspect a Cow for "
                              + $rootScope.globals.currentUser.client.name;
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.hrs = {};
        $scope.total = null;
        $scope.hr = {};
        $scope.base_url = "/assets/api/healthrecords/";
        $scope.client_url = $scope.base_url + "client/" + $scope.client + "/";
        $scope.url = null;
        $scope.inspect = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered HealthRecordListByClientController");

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
            $scope.herd = response.data.results;
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
        $scope.inspect = function () {
            var data = "client=" + $scope.globals.currentUser.client.name + "&"
                     + "recorded_by=" + $scope.globals.currentUser.username + "&"
                     + "inspection_time=" + convertDateTime($scope.inputTime) + "&"
                     + "cow=" + $scope.selectedCow.rfid + "&"
                     + "temperature=" + $scope.inputTemp + "&"
                     + "respiratory_rate=" + $scope.inputRR + "&"
                     + "heart_rate=" + $scope.inputHR + "&"
                     + "blood_pressure=" + $scope.inputBP + "&"
                     + "weight=" + $scope.inputWeight + "&"
                     + "body_condition_status=" + $scope.inputBCS + "&"
                     + "status=" + $scope.selectedStatus.name;
            if (typeof($scope.selectedIllness) == "object") {
                data += "&illness=" + $scope.selectedIllness.diagnosis; 
            }
            if (typeof($scope.selectedInjury) == "object") {
                data += "&injury=" + $scope.selectedInjury.diagnosis; 
            }
            if (typeof($scope.selectedTreatment) == "object") {
                data += "&treatment=" + $scope.selectedTreatment.name; 
            }
            if (typeof($scope.selectedVaccine) == "object") {
                data += "&vaccine=" + $scope.selectedVaccine.name; 
            }
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: $scope.base_url,
                data: data
            }).then(function (response) {
                $scope.hr = response.data;
                console.log("Created Health RecordID: " + $scope.hr.id);
                $location.url($scope.base_url + $scope.hr.id + "/results/");
            });
        };
});
