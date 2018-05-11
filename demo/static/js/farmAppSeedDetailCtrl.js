farmApp.controller("SeedDetailController",
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.inputId = $routeParams.seed_id;
        $scope.seed = null;
        $scope.base_url = "/assets/api/seeds/";
        $scope.plant = null;
        console.log("Entered SeedDetailController");

        $http({
            method: "GET",
            url: $scope.base_url + $scope.inputId + "/",
        }).then(function (response) {
            $scope.seed = response.data;
        });

        $scope.cereals = $rootScope.globals.cereals;
        $scope.grasses = $rootScope.globals.grasses;
        $scope.legumes = $rootScope.globals.legumes;
        $scope.plant = function (selectedCereal, selectedGrass, selectedLegume) {
            var data = {"id": $scope.seed.id,
                        "client": $scope.seed.client.name,
                        "seeded_by": $scope.seed.seeded_by,
                        "year": $scope.seed.year,
                        "season": $scope.seed.season.name,
                        "pasture": $scope.seed.pasture.name,
                        "cereal_hay": selectedCereal.name,
                        "grass_hay": selectedGrass.name,
                        "legume_hay": selectedLegume.name}
            console.log("data: " + data);
            $http({
                method: 'PUT',
                url: $scope.base_url + $scope.inputId + "/",
                data: JSON.stringify(data)
            }).then(function (response) {
                $scope.seed = response.data;
                console.log("Updated Seed ID: " + $scope.seed.id);
                $location.url($scope.base_url + $scope.seed.id + "/results/");
            });
        };
});
