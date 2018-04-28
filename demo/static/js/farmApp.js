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
