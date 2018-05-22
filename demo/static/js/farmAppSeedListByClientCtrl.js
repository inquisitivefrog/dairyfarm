farmApp.controller('SeedListByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.plant_header = "Plant Seeds for "
                            + $rootScope.globals.currentUser.client.name;
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.seeds = {};
        $scope.total = null;
        $scope.seed = null;
        $scope.base_url = "/assets/api/seeds/";
        $scope.client_url = $scope.base_url + "client/" + $scope.client + "/";
        $scope.url = null;
        $scope.plant = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered SeedListByClientController");

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
            $scope.seeds = response.data.results;
            $scope.total = response.data.count;
            if (($scope.offset == null) && ($scope.limit == null)) {
                // set beginning
                // assumes total > limit
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
        $scope.plant = function (inputYear) {
            var data = "client=" + $scope.globals.currentUser.client.name + "&"
                     + "seeded_by=" + $scope.globals.currentUser.username + "&"
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
