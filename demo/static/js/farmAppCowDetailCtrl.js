farmApp.controller("CowDetailController",
  function($scope, $http, $routeParams, $location) {
    $scope.cow_id = $routeParams.cow_id;
    $scope.cow = null;
    console.log("Entered CowDetailController");

    $http({
      method: "GET",
      url: "/assets/api/cows/" + $scope.cow_id + "/",
    }).then(function (response) {
      $scope.cow = response.data;
      $scope.inputId = $scope.cow_id;
      $scope.inputClient = $scope.cow.client.name;
      $scope.inputPurchaser = $scope.cow.purchased_by;
      $scope.inputDate = $scope.cow.purchase_date;
    });


    $http({
      method: 'GET',
      url: '/assets/api/ages/',
    }).then(function (response) {
      $scope.ages = response.data.results;
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

    $scope.update = function (selectedBreed, selectedColor, selectedAge) {
      var data = {"client": $scope.cow.client.name,
                  "purchased_by": $scope.cow.purchased_by,
                  "purchase_date": $scope.cow.purchase_date,
                  "breed": selectedBreed.name,
                  "color": selectedColor.name,
                  "age": selectedAge.name}
      $http({
        method: 'PUT',
        url: "/assets/api/cows/" + $scope.cow.id + "/",
        data: JSON.stringify(data)
      }).then(function (response) {
        $scope.cow = response.data;
        $location.url("/assets/api/cows/" + $scope.cow.id + "/");
      });
   };

});

