farmApp.controller('CowListController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.herd = {};
        $scope.total = null;
        $scope.cow = null;
        $scope.base_url = "/assets/api/cows/";
        $scope.url = null;
        $scope.purchase = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered CowListController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.base_url + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.base_url;
        }
        $http({
            method: 'GET',
            url: $scope.url,
        }).then(function (response) {
            $scope.herd = response.data.results;
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
        $scope.breeds = $rootScope.globals.breeds;
        $scope.colors = $rootScope.globals.colors;
        $scope.ages = $rootScope.globals.ages;
        $scope.purchase = function () {
            var data = "client=" + $scope.selectedClient.name + "&"
                     + "purchased_by=" + $scope.selectedPurchaser.username + "&"
                     + "purchase_date=" + convertDate($scope.inputDate) + "&"
                     + "breed=" + $scope.selectedBreed.name + "&"
                     + "color=" + $scope.selectedColor.name + "&"
                     + "age=" + $scope.selectedAge.name;
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: $scope.base_url,
                data: data
            }).then(function (response) {
                $scope.cow = response.data;
                console.log("Purchased Cow ID: " + $scope.cow.id);
                $location.url($scope.base_url + $scope.cow.id + "/results/");
            });
        };
    });
