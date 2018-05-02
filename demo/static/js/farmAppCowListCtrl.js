farmApp.controller('CowListController',
  function($scope, $http, $routeParams, $location) {
    $scope.offset = $routeParams.offset;
    $scope.limit = $routeParams.limit;
    $scope.herd = {};
    $scope.total = null;
    $scope.cow = null;
    $scope.url = "/assets/api/cows/";
    $scope.purchase = null;
    $scope.next = null;
    $scope.prev = null;
    $scope.selectedClient = null;
    console.log("Entered CowListController");

    $http({
      method: 'GET',
      url: '/assets/api/clients/',
    }).then(function (response) {
      $scope.clients = response.data.results;
      $scope.selectedClient = $scope.clients[0].name;
    });

    $http({
      method: 'GET',
      url: '/assets/api/users/',
    }).then(function (response) {
      $scope.users = response.data.results;
      $scope.selectedPurchaser = $scope.users[0].username;
    });

    $http({
      method: 'GET',
      url: '/assets/api/breeds/',
    }).then(function (response) {
      $scope.breeds = response.data.results;
    });

    $http({
      method: 'GET',
      url: '/assets/api/colors/',
    }).then(function (response) {
      $scope.colors = response.data.results;
    });

    $http({
      method: 'GET',
      url: '/assets/api/ages/',
    }).then(function (response) {
      $scope.ages = response.data.results;
    });

    if (($scope.offset != null) && ($scope.limit != null)) {
        $scope.url = "/assets/api/cows/" + farmAppString.setQueryString($scope.offset, $scope.limit);
    }
    console.log("url: " + $scope.url);
    $http({
      method: 'GET',
      url: $scope.url,
    }).then(function (response) {
      $scope.herd = response.data.results;
      $scope.total_cows = response.data.count;
      $scope.prev = response.data.previous;
      console.log("unformatted prev: " + $scope.prev);
      if ($scope.prev != null) {
          if (($scope.offset - $scope.limit) == 0) { 
              $scope.prev = "#" + $location.url;
          } else {
              $scope.prev = farmAppString.getURL($scope.prev) + farmAppString.getQueryString($scope.prev);
          }
      }
      $scope.next = response.data.next;
      if ($scope.next != null) {
          $scope.next = farmAppString.getURL($scope.next) + farmAppString.getQueryString($scope.next);
      }
      console.log("next: " + $scope.next);
      console.log("prev: " + $scope.prev);
    });

    //$scope.purchase = function (selectedClient, selectedPurchaser, inputDate, selectedBreed, selectedColor, selectedAge) {
    $scope.purchase = function () {
      //var data = "client=" + selectedClient.name + "&"
      //         + "purchased_by=" + selectedPurchaser.username + "&"
      //         + "purchase_date=" + inputDate + "&"
      //         + "breed=" + selectedBreed.name + "&"
      //         + "color=" + selectedColor.name + "&"
      //         + "age=" + selectedAge.name;
      var data = "client=" + $scope.selectedClient.name + "&"
               + "purchased_by=" + $scope.selectedPurchaser.username + "&"
               + "purchase_date=" + $scope.inputDate + "&"
               + "breed=" + $scope.selectedBreed.name + "&"
               + "color=" + $scope.selectedColor.name + "&"
               + "age=" + $scope.selectedAge.name;
      console.log("data: " + data);
      $http({
        method: 'POST',
        url: "/assets/api/cows/",
        data: data
      }).then(function (response) {
        $scope.cow = response.data;
        //$location.url("/assets/api/cows/" + $scope.cow.id + "/");
        $http({
          method: 'GET',
          url: "/assets/api/cows/" + $scope.cow.id + "/"
        }).then(function (response) {
          $scope.cow = response.data;
          //$location.url("/assets/api/cows/" + $scope.cow.id + "/");
        });
      });
   };
});
