farmApp.controller('HealthRecordListController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.hrs = {};
        $scope.total = null;
        $scope.hr = null;
        $scope.base_url = "/assets/api/healthrecords/";
        $scope.url = null;
        $scope.inspect = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered HealthRecordListController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.base_url + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.base_url;
        }
        $http({
            method: 'GET',
            url: $scope.url,
        }).then(function (response) {
            $scope.hrs = response.data.results;
            $scope.total = response.data.count;
            if (($scope.offset == null) && ($scope.limit == null)) {
                // set beginning
                $scope.offset = $rootScope.globals.limit;
                $scope.limit = $rootScope.globals.limit;
                $scope.next = "#" + $scope.base_url + "limit/" + $scope.limit + "/offset/" + $scope.offset + "/";
                delete $scope.prev;
            } else {
                offset = parseInt($scope.offset) + parseInt($scope.limit);
                if (offset < parseInt($scope.total)) {
                    $scope.next = "#" + $scope.base_url + "limit/" + $scope.limit + "/offset/" + offset + "/";
                } else {
                    delete $scope.next;
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
        $scope.statuses = $rootScope.globals.statuses;
        $scope.illnesses = $rootScope.globals.illnesses;
        $scope.injuries = $rootScope.globals.injuries;
        $scope.treatments = $rootScope.globals.treatments;
        $scope.vaccines = $rootScope.globals.vaccines;
        $scope.inspect = function () {
        var data = "client=" + $scope.selectedClient.name + "&"
                 + "recorded_by=" + $scope.selectedRecorder.username + "&"
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
