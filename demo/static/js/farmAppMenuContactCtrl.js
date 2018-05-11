farmApp.controller('MenuContactController',
  function($scope, $http) {
      console.log('Entered MenuContactController');

    $http({
        method: 'GET',
        url: '/contact/',
    }).then(function (response) {
        $scope.data = response.data;
        console.log("data: " + $scope.data);
    });
});
