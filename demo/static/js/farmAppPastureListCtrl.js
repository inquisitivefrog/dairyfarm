farmApp.controller('PastureListController',
  function($scope, $rootScope, $http, $routeParams, $location) {
        $scope.offset = $routeParams.offset;
        $scope.limit = $routeParams.limit;
        $scope.pastures = {};
        $scope.total = null;
        $scope.pasture = null;
        $scope.base_url = "/assets/api/pastures/";
        $scope.url = null;
        $scope.cultivate = null;
        $scope.next = null;
        $scope.prev = null;
        console.log("Entered PastureListController");

        if (($scope.offset != null) && ($scope.limit != null)) {
            $scope.url = $scope.base_url + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        } else {
            $scope.url = $scope.base_url;
        }
        $http({
            method: 'GET',
            url: $scope.url,
        }).then(function (response) {
            $scope.pastures = response.data.results;
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

        $scope.cultivate = function (inputName, inputFallow) {
            var data = "client=" + $scope.selectedClient.name + "&"
                     + "name=" + inputName + "&"
                     + "fallow=" + inputFallow + "&"
                     + "distance=" + $scope.inputDistance + "&"
                     + "url=/static/images/regions/" + farmAppString.bs2uc(inputName) + ".jpg";
            console.log("data: " + data);
            $http({
                method: 'POST',
                url: $scope.base_url,
                data: data
            }).then(function (response) {
                $scope.pasture = response.data;
                console.log("Created Pasture ID: " + $scope.pasture.id);
                $location.url($scope.base_url + $scope.pasture.id + "/results/");
            });
        };
});
