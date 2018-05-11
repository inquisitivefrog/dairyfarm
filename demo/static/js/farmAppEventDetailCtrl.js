farmApp.controller("EventDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.event_id;
        $scope.event = null;
        $scope.base_url = "/assets/api/events/";
        console.log("Entered EventDetailController");

        $scope.actions = $rootScope.globals.actions;

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.event = response.data;
        });

        $scope.update = function (selectedAction) {
            var data = {"id": $scope.event.id,
                        "cow": $scope.event.cow.rfid,
                        "client": $scope.event.client.name,
                        "recorded_by": $scope.event.recorded_by,
                        "event_time": $scope.event.event_time,
                        "action": selectedAction.name}
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.event = response.data;
                console.log("Updated Event ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };
    });
