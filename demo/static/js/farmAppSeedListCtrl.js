farmApp.controller('SeedListController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.seeds = {};
        $scope.total = null;
        $scope.seed = null;
        $scope.base_url = "/assets/api/seeds/";
        $scope.url = null;
        $scope.plant = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered SeedListController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.base_url + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.base_url;
        }
        $http({
            method: 'GET',
            url: $scope.url,
        }).then(function (response) {
            $scope.seeds = response.data.results;
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
        $scope.pastures = $rootScope.globals.pastures;
        $scope.seasons = $rootScope.globals.seasons;
        $scope.cereals = $rootScope.globals.cereals;
        $scope.grasses = $rootScope.globals.grasses;
        $scope.legumes = $rootScope.globals.legumes;
        $scope.plant = function (inputYear) {
        var data = "client=" + $scope.selectedClient.name + "&"
                 + "seeded_by=" + $scope.selectedSeededBy.username + "&"
                 + "year=" + inputYear + "&"
                 + "pasture=" + $scope.selectedPasture.name + "&"
                 + "season=" + $scope.selectedSeason.name + "&"
                 + "cereal_hay=" + $scope.selectedCereal.name + "&"
                 + "grass_hay=" + $scope.selectedGrass.name + "&"
                 + "legume_hay=" + $scope.selectedLegume.name;
        console.log("data: " + data);
        $http({
            method: 'POST',
            url: $scope.base_url,
            data: data
        }).then(function (response) {
            $scope.seed = response.data;
            console.log("Created Seed ID: " + $scope.seed.id);
            $location.url($scope.base_url + $scope.seed.id + "/results/");
        });
    };
});
