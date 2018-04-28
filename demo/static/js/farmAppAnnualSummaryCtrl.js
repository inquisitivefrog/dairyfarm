farmApp.controller('AnnualSummaryController',
  function($scope, $http) {
    $scope.rows = [];
    $scope.response = null;
    console.log('Entered AnnualSummaryController');

    $http({
          method: 'GET',
          url: '/summary/api/annual/',
    }).then(function (response) {
          $scope.response = response;
          $scope.rows = response.data;
    });
});
