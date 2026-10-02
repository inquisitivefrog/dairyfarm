farmApp.controller('TestsController',
  function($scope, $routeParams) {
    console.log('Entered TestsController');
    var filter = $routeParams.filter || 'all';
    var knownFilters = [
      'suite-assets-tests-test-api-views',
      'suite-assets-tests-test-models',
      'suite-assets-tests-test-serializers',
      'suite-assets-tests-test-tenant-isolation',
      'suite-assets-tests-test-ui-auth',
      'suite-assets-tests-test-urls',
      'suite-assets-tests-test-user-api',
      'suite-assets-tests-test-user-creation-tool',
      'suite-assets-tests-test-views',
      'suite-summary-tests-test-api-views',
      'suite-summary-tests-test-models',
      'suite-summary-tests-test-serializers',
      'suite-summary-tests-test-urls'
    ];
    $scope.testResultsFilter =
      knownFilters.indexOf(filter) === -1 ? 'all' : filter;
    $scope.setTestResultsFilter = function(filter) {
      $scope.testResultsFilter = filter;
    };
});
