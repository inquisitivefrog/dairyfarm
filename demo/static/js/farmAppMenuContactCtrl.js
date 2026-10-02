farmApp.controller('MenuContactController',
  function($scope, $http, $httpParamSerializer) {
    $scope.contact = {};
    $scope.submitting = false;

    $http({
        method: 'GET',
        url: '/contact/',
    }).then(function (response) {
        $scope.contactReady = true;
    }, function () {
        $scope.contactError = "The contact form could not be loaded.";
    });

    $scope.submitContact = function (form) {
        if (form.$invalid || $scope.submitting) {
            return;
        }

        $scope.submitting = true;
        $scope.contactError = null;
        $http({
            method: 'POST',
            url: '/contact/',
            data: $httpParamSerializer({
                contact_name: $scope.contact.name,
                contact_email: $scope.contact.email,
                content: $scope.contact.content
            })
        }).then(function () {
            $scope.contact = {};
            form.$setPristine();
            form.$setUntouched();
            $scope.contactSent = true;
        }, function () {
            $scope.contactError = "Your message could not be sent. Please try again.";
        }).finally(function () {
            $scope.submitting = false;
        });
    };
});
