farmApp.controller("HealthRecordDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.hr_id;
        $scope.hr = null;
        $scope.update = null;
        $scope.update_header = "Update Health Record for "
                             + $rootScope.globals.currentUser.client.name;
        $scope.base_url = "/assets/api/healthrecords/";
        console.log("Entered HealthRecordDetailController");

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.hr = response.data;
        });

        $scope.globals = $rootScope.globals;
        $scope.update = function (selectedStatus, selectedIllness, selectedInjury, selectedTreatment, selectedVaccine) {
            var data = {"id": $scope.hr.id,
                        "cow": $scope.hr.cow.rfid,
                        "client": $scope.hr.client.name,
                        "recorded_by": $scope.hr.recorded_by,
                        "inspection_time": $scope.hr.inspection_time,
                        "temperature": $scope.inputTemp,
                        "respiratory_rate": $scope.inputRR,
                        "heart_rate": $scope.inputHR,
                        "blood_pressure": $scope.inputBP,
                        "weight": $scope.inputWeight,
                        "body_condition_status": $scope.inputBCS,
                        "status": selectedStatus.name}
            if (typeof(selectedIllness) == "object") {
                data["illness"] = selectedIllness.diagnosis;
            }
            if (typeof(selectedInjury) == "object") {
                data["injury"] = selectedInjury.diagnosis;
            }
            if (typeof(selectedTreatment) == "object") {
                data["treatment"] = selectedTreatment.name;
            }
            if (typeof(selectedVaccine) == "object") {
                data["vaccine"] = selectedVaccine.name;
            }
            console.log("data: " + JSON.stringify(data));
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.hr = response.data;
                console.log("Updated Health Record ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };
    });
