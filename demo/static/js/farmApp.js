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
    $routeProvider
    //.when("/", {
    //      templateUrl: "/static/templates/index_blank.html",
    //      controller: "IndexController"
    //})
    .when("/index/", {
          templateUrl: "/static/templates/index.html",
          controller: "IndexController"
          //templateUrl: "/static/templates/annual_report.html",
          //controller: "AnnualSummaryController"
    })
    .when("/login/", {
          templateUrl: "/static/templates/auth_login.html",
          controller: "LoginController"
    })
    .when("/logout/", {
          templateUrl: "/static/templates/auth_logged_out.html",
          controller: "LogoutController"
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
    .when("/summary/", {
          templateUrl: "/static/templates/annual_report.html",
          controller: "AnnualSummaryController"
    })
    .when("/summary/api/monthly/:year/", {
          templateUrl: "/static/templates/annual_by_month_report.html",
          controller: "MonthlySummaryController"
    })
    .when("/summary/api/monthly/:year/:month/", {
          templateUrl: "/static/templates/monthly_report.html",
          controller: "MonthlySummaryController"
    })
    .when("/assets/api/cows/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListController"
    })
    .when("/assets/api/cows/limit/:limit/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListController"
    })
    .when("/assets/api/cows/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/cow_list.html",
          controller: "CowListController"
    })
    .when("/assets/api/cows/:cow_id/results/", {
          templateUrl: "/static/templates/cow_results.html",
          controller: "CowResultsController"
    })
    .when("/assets/api/cows/:cow_id/", {
          templateUrl: "/static/templates/cow_detail.html",
          controller: "CowDetailController"
    })
    .when("/assets/api/events/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListController"
    })
    .when("/assets/api/events/limit/:limit/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListController"
    })
    .when("/assets/api/events/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListController"
    })
    .when("/assets/api/events/:event_id/", {
          templateUrl: "/static/templates/event_detail.html",
          controller: "EventDetailController"
    })
    .when("/assets/api/events/:event_id/results/", {
          templateUrl: "/static/templates/event_results.html",
          controller: "EventResultsController"
    })
    .when("/assets/api/exercises/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListController"
    })
    .when("/assets/api/exercises/limit/:limit/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListController"
    })
    .when("/assets/api/exercises/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListController"
    })
    .when("/assets/api/exercises/:exercise_id/", {
          templateUrl: "/static/templates/exercise_detail.html",
          controller: "ExerciseDetailController"
    })
    .when("/assets/api/exercises/:exercise_id/results/", {
          templateUrl: "/static/templates/exercise_results.html",
          controller: "ExerciseResultsController"
    })
    .when("/assets/api/healthrecords/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListController"
    })
    .when("/assets/api/healthrecords/limit/:limit/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListController"
    })
    .when("/assets/api/healthrecords/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListController"
    })
    .when("/assets/api/healthrecords/:hr_id/", {
          templateUrl: "/static/templates/healthrecord_detail.html",
          controller: "HealthRecordDetailController"
    })
    .when("/assets/api/healthrecords/:hr_id/results/", {
          templateUrl: "/static/templates/healthrecord_results.html",
          controller: "HealthRecordResultsController"
    })
    .when("/assets/api/milk/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListController"
    })
    .when("/assets/api/milk/limit/:limit/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListController"
    })
    .when("/assets/api/milk/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListController"
    })
    .when("/assets/api/milk/:milk_id/", {
          templateUrl: "/static/templates/milk_detail.html",
          controller: "MilkDetailController"
    })
    .when("/assets/api/milk/:milk_id/results/", {
          templateUrl: "/static/templates/milk_results.html",
          controller: "MilkResultsController"
    })
    .when("/assets/api/pastures/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListController"
    })
    .when("/assets/api/pastures/limit/:limit/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListController"
    })
    .when("/assets/api/pastures/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListController"
    })
    .when("/assets/api/pastures/:pasture_id/", {
          templateUrl: "/static/templates/pasture_detail.html",
          controller: "PastureDetailController"
    })
    .when("/assets/api/pastures/:pasture_id/results/", {
          templateUrl: "/static/templates/pasture_results.html",
          controller: "PastureResultsController"
    })
    .when("/assets/api/seeds/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListController"
    })
    .when("/assets/api/seeds/limit/:limit/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListController"
    })
    .when("/assets/api/seeds/limit/:limit/offset/:offset/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListController"
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
    $rootScope.globals["limit"] = 10;
    console.log("globals: " + Object.getOwnPropertyNames($rootScope.globals));
    console.log("globals limit: " + $rootScope.globals.limit);

    if ($rootScope.globals.currentUser) {
        var auth = 'Basic ' + $rootScope.globals.currentUser.authdata;
        $http.defaults.headers.common['Authorization'] = auth;
        console.log("auth: " + auth);
    }
 
    $rootScope.$on('$locationChangeStart', function (event, next, current) {
        // redirect to login page if not logged in
        if ($location.path() !== '/login/' && !$rootScope.globals.currentUser) {
            $location.path('/login/');
        }
    });
});
