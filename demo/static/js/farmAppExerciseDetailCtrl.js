farmApp.controller("ExerciseDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.exercise_id;
        $scope.exercise = null;
        $scope.base_url = "/assets/api/exercises/";
        console.log("Entered ExerciseDetailController");

        $scope.pastures = $rootScope.globals.pastures;

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.exercise = response.data;
        });

        $scope.update = function (selectedPasture) {
            var data = {"id": $scope.exercise.id,
                        "cow": $scope.exercise.cow.rfid,
                        "client": $scope.exercise.client.name,
                        "recorded_by": $scope.exercise.recorded_by,
                        "exercise_time": $scope.exercise.exercise_time,
                        "pasture": selectedPasture.name}
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.exercise = response.data;
                console.log("Updated Exercise ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };
    });
