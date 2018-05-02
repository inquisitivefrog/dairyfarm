var farmApp = angular.module("farmApp", ["ngRoute", "Authentication", "Home", "ngCookies"]);

farmApp.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    var ctype = "application/x-www-form-urlencoded;charset=utf-8"; 
    $httpProvider.defaults.headers.post["Content-Type"] = ctype;
});

farmApp.config(function ($routeProvider) {
      $routeProvider
      .when("/login/", {
          templateUrl: "/static/templates/auth_login.html",
          controller: "LoginController",
      })
      .when("/logout/", {
          templateUrl: "/static/templates/auth_logged_out.html",
          controller: "LogoutController"
      })
      .when("/", {
          //templateUrl: "/static/templates/index.html",
          //controller: "IndexController"
          templateUrl: "/static/templates/annual_report.html",
          controller: "AnnualSummaryController"
      })
      .when("/docs/mrd/", {
          templateUrl: "/static/templates/docs_mrd.html",
          controller: "MRDController"
      })
      .when("/docs/mrd/strategy/", {
          templateUrl: "/static/templates/docs_mrd.html#strategy",
          controller: "MRDController"
      })
      .when("/docs/mrd/bm/", {
          templateUrl: "/static/templates/docs_mrd.html#bm",
          controller: "MRDController"
      })
      .when("/docs/mrd/groups/", {
          templateUrl: "/static/templates/docs_mrd.html#groups",
          controller: "MRDController"
      })
      .when("/docs/mrd/bom/", {
          templateUrl: "/static/templates/docs_mrd.html#bom",
          controller: "MRDController"
      })
      .when("/docs/mrd/internal/", {
          templateUrl: "/static/templates/docs_mrd.html#internal",
          controller: "MRDController"
      })
      .when("/docs/mrd/external/", {
          templateUrl: "/static/templates/docs_mrd.html#external",
          controller: "MRDController"
      })
      .when("/docs/mrd/tbd/", {
          templateUrl: "/static/templates/docs_mrd.html#tbm",
          controller: "MRDController"
      })
      .when("/docs/dd_assets/", {
          templateUrl: "/static/templates/docs_dd_assets.html",
          controller: "DDAssetsController"
      })
      .when("/docs/dd_assets/", {
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
      .when("/assets/api/cows/error/", {
          templateUrl: "/static/templates/cow_error.html",
          controller: "CowListController"
      })
      .when("/assets/api/cows/results/", {
          templateUrl: "/static/templates/cow_results.html",
          controller: "CowListController"
      })
      .when("/assets/api/cows/:cow_id/", {
          templateUrl: "/static/templates/cow_detail.html",
          controller: "CowDetailController"
      })
      .when("/assets/api/events/", {
          templateUrl: "/static/templates/event_list.html",
          controller: "EventListController"
      })
      .when("/assets/api/events/:event_id/", {
          templateUrl: "/static/templates/event_detail.html",
          controller: "EventDetailController"
      })
      .when("/assets/api/exercises/", {
          templateUrl: "/static/templates/exercise_list.html",
          controller: "ExerciseListController"
      })
      .when("/assets/api/exercises/:exercise_id/", {
          templateUrl: "/static/templates/exercise_detail.html",
          controller: "ExerciseDetailController"
      })
      .when("/assets/api/healthrecords/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListController"
      })
      .when("/assets/api/healthrecords/:hr_id/", {
          templateUrl: "/static/templates/healthrecord_detail.html",
          controller: "HealthRecordDetailController"
      })
      .when("/assets/api/milk/", {
          templateUrl: "/static/templates/milk_list.html",
          controller: "MilkListController"
      })
      .when("/assets/api/milk/:milk_id/", {
          templateUrl: "/static/templates/milk_detail.html",
          controller: "MilkDetailController"
      })
      .when("/assets/api/pastures/", {
          templateUrl: "/static/templates/pasture_list.html",
          controller: "PastureListController"
      })
      .when("/assets/api/pastures/:pasture_id/", {
          templateUrl: "/static/templates/pasture_detail.html",
          controller: "PastureDetailController"
      })
      .when("/assets/api/seeds/", {
          templateUrl: "/static/templates/seed_list.html",
          controller: "SeedListController"
      })
      .when("/assets/api/seeds/:seed_id/", {
          templateUrl: "/static/templates/seed_detail.html",
          controller: "SeedDetailController"
      })
      .when("/assets/api/cows/:cow_id/results/", {
          templateUrl: "/static/templates/herd_results.html",
          controller: "HerdController"
      })
      .otherwise({
          redirectTo: '/login/'
      });
});

farmApp.run(function ("$rootScope", "$location", "$cookieStore", "$http") {
    $rootScope.globals = $cookieStore.get("globals") || {};
    if ($rootScope.globals.currentUser) {
        $http.defaults.headers.common["Authorization"] = "Basic " + $rootScope.globals.currentUser.authdata;
    }
    
   // var routesThatDontRequireAuth = ['/login/'];

   // var routeClean = function (route) {
   //     return _.find(routesThatDontRequireAuth,
   //         function (noAuthRoute) {
   //             return _.str.startsWith(route, noAuthRoute);
   //     });
   // };
   
    $rootScope.$on("$locationChangeStart", function (event, next, current) {
        // when route requires auth but user is not logged in
        if ($location.path() !== "/login/" && !$rootScope.globals.currentUser) {
            $location.path('/login/')
        }
    });
});
