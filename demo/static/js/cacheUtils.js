var dependentData = {load: null};

dependentData.load = function($http, $rootScope) {
    console.log("Entered dependentData.load");

    $http({
        method: "GET",
        url: "/assets/api/clients/?limit=50",
    }).then(function (response) {
        $rootScope.globals.clients = response.data.results;
    });

    console.log("dependentData loaded: " + Object.getOwnPropertyNames($rootScope.globals));
    return;
}
