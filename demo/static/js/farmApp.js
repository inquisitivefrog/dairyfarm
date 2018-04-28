var farmApp = angular.module("farmApp", ["ngRoute"]);

farmApp.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    var ctype = "application/x-www-form-urlencoded;charset=utf-8"; 
    $httpProvider.defaults.headers.post["Content-Type"] = ctype;
});

farmApp.config(function ($routeProvider) {
      $routeProvider
      .when("/", {
          templateUrl: "/static/templates/index.html",
          controller: "IndexController"
      })
      .when("/docs/mrd/", {
          templateUrl: "/static/templates/mrd.html",
          controller: "MRDController"
      })
      .when("/docs/mrd/strategy/", {
          templateUrl: "/static/templates/mrd.html#strategy",
          controller: "MRDController"
      })
      .when("/docs/mrd/bm/", {
          templateUrl: "/static/templates/mrd.html#bm",
          controller: "MRDController"
      })
      .when("/docs/mrd/groups/", {
          templateUrl: "/static/templates/mrd.html#groups",
          controller: "MRDController"
      })
      .when("/docs/mrd/bom/", {
          templateUrl: "/static/templates/mrd.html#bom",
          controller: "MRDController"
      })
      .when("/docs/mrd/internal/", {
          templateUrl: "/static/templates/mrd.html#internal",
          controller: "MRDController"
      })
      .when("/docs/mrd/external/", {
          templateUrl: "/static/templates/mrd.html#external",
          controller: "MRDController"
      })
      .when("/docs/mrd/tbd/", {
          templateUrl: "/static/templates/mrd.html#tbm",
          controller: "MRDController"
      })
      .when("/docs/dd_assets/", {
          templateUrl: "/static/templates/dd_assets.html",
          controller: "DDAssetsController"
      })
      .when("/docs/dd_assets/", {
          templateUrl: "/static/templates/dd_assets.html",
          controller: "DDAssetsController"
      })
      .when("/docs/dd_summary/", {
          templateUrl: "/static/templates/dd_summary.html",
          controller: "DDSummaryController"
      })
      .when("/docs/tests/", {
          templateUrl: "/static/templates/tests.html",
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
      .when("/assets/api/healthrecords/", {
          templateUrl: "/static/templates/healthrecord_list.html",
          controller: "HealthRecordListController"
      })
      .when("/assets/api/healthrecords/:hr_id/", {
          templateUrl: "/static/templates/healthrecord_detail.html",
          controller: "HealthRecordDetailController"
      })
      .when("/assets/api/cows/:cow_id/results/", {
          templateUrl: "/static/templates/herd_results.html",
          controller: "HerdController"
      });
});
