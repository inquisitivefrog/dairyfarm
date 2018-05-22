var farmApp = angular.module("farmApp", ["ngRoute", "ngCookies"]);

farmApp.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    var ctype = "application/x-www-form-urlencoded;charset=utf-8"; 
    $httpProvider.defaults.headers.post["Content-Type"] = ctype;
    $httpProvider.defaults.headers.post["Cache-Control"] = "private";
});

farmApp.config(function ($routeProvider, $locationProvider) {
    //$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
    //$httpProvider.defaults.cache = true;
    $routeProvider
    .when("/home/", {
          templateUrl: "/static/templates/annual_report.html",
          controller: "AnnualSummaryByClientController"
    })
    .when("/login/", {
          templateUrl: "/static/templates/auth_login.html",
          controller: "LoginController"
    })
    .when("/logout/", {
          templateUrl: "/static/templates/auth_logged_out.html",
          controller: "LogoutController"
    })
    .when("/cache/", {
          templateUrl: "/static/templates/cache.html",
          controller: "ReloadCacheController"
    })
    .when("/cache/:quiet/", {
          templateUrl: "/static/templates/cache.html",
          controller: "ReloadCacheController"
    })
    .when("/about/", {
          templateUrl: "/static/templates/menu_about.html",
          controller: "MenuAboutController"
    })
    .when("/contact/", {
          templateUrl: "/static/templates/menu_contact.html",
          controller: "MenuContactController"
    })
    .when("/docs/mrd/", {
          templateUrl: "/static/templates/docs_mrd.html",
          controller: "MRDController"
    })
    .when("/docs/dd_assets/", {
          templateUrl: "/static/templates/docs_dd_assets.html",
          controller: "DDAssetsController"
    })
    .when("/docs/dd_assets/:section/", {
          templateUrl: "/static/templates/docs_dd_assets.html",
          controller: "DDAssetsController"
    })
    .when("/docs/dd_summary/", {
          templateUrl: "/static/templates/docs_dd_summary.html",
          controller: "DDSummaryController"
    })
    .when("/docs/tests/", {
          templateUrl: "/static/templates/docs_tests.html",
          controller: "TestsController"
    })
    .when("/summary/api/annual/", {
          templateUrl: "/static/templates/annual_report.html",
          controller: "AnnualSummaryByClientController"
    })
    .when("/summary/api/annual/client/:client/", {
          templateUrl: "/static/templates/annual_report.html",
          controller: "AnnualSummaryByClientController"
    })
    //.when("/summary/api/annual/client/:client/year/:year/", {
    //      templateUrl: "/static/templates/annual_report.html",
    //      controller: "AnnualSummaryByClientController"
    //})
    .when("/summary/api/monthly/client/:client/year/:year/", {
          templateUrl: "/static/templates/annual_by_month_report.html",
          controller: "MonthlySummaryByClientController"
    })
    .when("/summary/api/monthly/client/:client/year/:year/month/:month/", {
          templateUrl: "/static/templates/monthly_report.html",
          controller: "MonthlySummaryByClientController"
    })
    .when("/assets/api/cows/client/:client/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListByClientController"
    })
    .when("/assets/api/cows/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListByClientController"
    })
    .when("/assets/api/cows/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListByClientController"
    })
    .when("/assets/api/cows/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListByClientController"
    })
    .when("/assets/api/cows/:cow_id/results/", {
          templateUrl: "/static/templates/cow_results.html",
          controller: "CowResultsController"
    })
    .when("/assets/api/cows/:cow_id/", {
          templateUrl: "/static/templates/cow_detail.html",
          controller: "CowDetailController"
    })
    .when("/assets/api/events/client/:client/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListByClientController"
    })
    .when("/assets/api/events/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListByClientController"
    })
    .when("/assets/api/events/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListByClientController"
    })
    .when("/assets/api/events/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListByClientController"
    })
    .when("/assets/api/events/:event_id/", {
          templateUrl: "/static/templates/event_detail.html",
          controller: "EventDetailController"
    })
    .when("/assets/api/events/:event_id/results/", {
          templateUrl: "/static/templates/event_results.html",
          controller: "EventResultsController"
    })
    .when("/assets/api/exercises/client/:client/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListByClientController"
    })
    .when("/assets/api/exercises/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListByClientController"
    })
    .when("/assets/api/exercises/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListByClientController"
    })
    .when("/assets/api/exercises/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListByClientController"
    })
    .when("/assets/api/exercises/:exercise_id/", {
          templateUrl: "/static/templates/exercise_detail.html",
          controller: "ExerciseDetailController"
    })
    .when("/assets/api/exercises/:exercise_id/results/", {
          templateUrl: "/static/templates/exercise_results.html",
          controller: "ExerciseResultsController"
    })
    .when("/assets/api/healthrecords/client/:client/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListByClientController"
    })
    .when("/assets/api/healthrecords/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListByClientController"
    })
    .when("/assets/api/healthrecords/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListByClientController"
    })
    .when("/assets/api/healthrecords/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListByClientController"
    })
    .when("/assets/api/healthrecords/:hr_id/", {
          templateUrl: "/static/templates/healthrecord_detail.html",
          controller: "HealthRecordDetailController"
    })
    .when("/assets/api/healthrecords/:hr_id/results/", {
          templateUrl: "/static/templates/healthrecord_results.html",
          controller: "HealthRecordResultsController"
    })
    .when("/assets/api/milk/client/:client/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListByClientController"
    })
    .when("/assets/api/milk/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListByClientController"
    })
    .when("/assets/api/milk/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListByClientController"
    })
    .when("/assets/api/milk/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListByClientController"
    })
    .when("/assets/api/milk/:milk_id/", {
          templateUrl: "/static/templates/milk_detail.html",
          controller: "MilkDetailController"
    })
    .when("/assets/api/milk/:milk_id/results/", {
          templateUrl: "/static/templates/milk_results.html",
          controller: "MilkResultsController"
    })
    .when("/assets/api/pastures/client/:client/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListByClientController"
    })
    .when("/assets/api/pastures/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListByClientController"
    })
    .when("/assets/api/pastures/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListByClientController"
    })
    .when("/assets/api/pastures/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListByClientController"
    })
    .when("/assets/api/pastures/:pasture_id/", {
          templateUrl: "/static/templates/pasture_detail.html",
          controller: "PastureDetailController"
    })
    .when("/assets/api/pastures/:pasture_id/results/", {
          templateUrl: "/static/templates/pasture_results.html",
          controller: "PastureResultsController"
    })
    .when("/assets/api/seeds/client/:client/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListByClientController"
    })
    .when("/assets/api/seeds/client/:client/limit/:limit/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListByClientController"
    })
    .when("/assets/api/seeds/client/:client/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListByClientController"
    })
    .when("/assets/api/seeds/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListByClientController"
    })
    .when("/assets/api/seeds/:seed_id/", {
          templateUrl: "/static/templates/seed_detail.html",
          controller: "SeedDetailController"
    })
    .when("/assets/api/seeds/:seed_id/results/", {
          templateUrl: "/static/templates/seed_results.html",
          controller: "SeedResultsController"
    })
});

farmApp.run(function($rootScope, $location, $http, $cookies) {
    $rootScope.globals = $cookies.get('globals') || {};
    console.log("globals set: " + Object.getOwnPropertyNames($rootScope.globals));

    console.log("currentUser: " + $rootScope.globals.currentUser);
    $rootScope.$on('$locationChangeStart', function (event, next, current) {
        // redirect to login page if not logged in or attempts page refresh
        if ($location.path() !== '/login/' && !$rootScope.globals.currentUser) {
            console.log("forced relogin");
            $location.path('/login/');
        }
    });
});
