farmApp.controller("MilkDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.milk_id;
        $scope.milk = null;
        $scope.update = null;
        $scope.base_url = "/assets/api/milk/";
        console.log("Entered MilkDetailController");

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.milk = response.data;
        });

        $scope.update = function (inputGallons) {
            var data = {"id": $scope.milk.id,
                        "cow": $scope.milk.cow.rfid,
                        "client": $scope.milk.client.name,
                        "recorded_by": $scope.milk.recorded_by,
                        "milking_time": $scope.milk.milking_time,
                        "gallons": inputGallons}
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.milk = response.data;
                console.log("Updated Milk ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };
    });
