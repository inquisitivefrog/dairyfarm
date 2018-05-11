farmApp.controller("PastureDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.pasture_id;
        $scope.pasture = null;
        $scope.base_url = "/assets/api/pastures/";
        $scope.cultivate = null;
        console.log("Entered PastureDetailController");

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.pasture = response.data;
        });

        $scope.clients = $rootScope.globals.clients;

        $scope.cultivate = function (inputName, inputFallow, inputDistance) {
            var data = {"id": $scope.pasture.id,
                        "client": $scope.pasture.client.name,
                        "name": inputName,
                        "fallow": inputFallow,
                        "distance": inputDistance,
                        "url": "/static/images/regions/" + farmAppString.bs2uc(inputName) + ".jpg"}
            console.log("data: " + data);
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.pasture = response.data;
                console.log("Updated Pasture ID: " + $scope.pasture.id);
                $location.url($scope.base_url + $scope.pasture.id + "/results/");
            });
        };
});
