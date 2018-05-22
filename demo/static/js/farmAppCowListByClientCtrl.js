farmApp.controller('CowListByClientController',
    function($scope, $rootScope, $http, $routeParams, $location) {
        if ($routeParams.client != null) {
            $scope.client = $routeParams.client;
        } else {
            $scope.client = $rootScope.globals.currentUser.client.id;
        }
        $scope.purchase_header = "Purchase a Cow for "
                               + $rootScope.globals.currentUser.client.name;
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.herd = {};
        $scope.total = null;
        $scope.cow = null;
        $scope.base_url = "/assets/api/cows/";
        $scope.client_url = $scope.base_url + "client/" + $scope.client + "/";
        $scope.url = null;
        $scope.purchase = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered CowListByClientController");

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
            $scope.herd = response.data.results;
            $scope.total = response.data.count;
            if (($scope.offset == null) && ($scope.limit == null)) {
                // set beginning
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
        $scope.purchase = function () {
            var data = "client=" + $scope.globals.currentUser.client.name + "&"
                     + "purchased_by=" + $scope.globals.currentUser.username + "&"
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
