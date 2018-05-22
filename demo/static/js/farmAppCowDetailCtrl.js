farmApp.controller("CowDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.cow_id;
        $scope.cow = null;
        $scope.base_url = "/assets/api/cows/";
        $scope.today = currentDate();
        console.log("Entered CowDetailController");

        $scope.globals = $rootScope.globals;

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.cow = response.data;
        });

        $scope.update = function (selectedBreed, selectedColor, selectedAge) {
            var data = {"id": $scope.cow.id,
                        "rfid": $scope.cow.rfid,
                        "client": $scope.cow.client.name,
                        "purchased_by": $scope.cow.purchased_by,
                        "purchase_date": $scope.cow.purchase_date,
                        "breed": selectedBreed.name,
                        "color": selectedColor.name,
                        "age": selectedAge.name}
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.cow = response.data;
                console.log("Updated Cow ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };

        $scope.sell = function () {
            $http({
                method: 'DELETE',
                url: $scope.base_url + $scope.inputId + "/",
            }).then(function (response) {
                $scope.cow = response.data;
                console.log("Sold Cow ID: " + $scope.inputId);
                $location.url($scope.base_url + $scope.inputId + "/results/");
            });
        };
    });
