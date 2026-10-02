farmApp.controller("ClientSelectionController",
    function ($scope, $rootScope, $location, $timeout) {
        $scope.globals = $rootScope.globals;
        $scope.clientSelection = {selectedClientId: null};
        $scope.pendingDocumentationSection = null;
        $scope.pendingDocumentationNavigation = false;

        $scope.$watch("globals.currentUser", function (user) {
            if (user && user.client) {
                $scope.clientSelection.selectedClientId = user.client.id;
            }
        });

        $scope.selectClient = function () {
            var clients = $scope.globals.currentUser.clients;
            var selected = clients.filter(function (client) {
                return client.id ===
                    $scope.clientSelection.selectedClientId;
            })[0];

            if (!selected) {
                return;
            }

            $scope.globals.currentUser.client = selected;
            $location.url("/cache/switch/");
        };

        $scope.openDocumentation = function (path, section, event) {
            if (event) {
                event.preventDefault();
            }

            var sameDocument = $location.path() === path;
            $scope.pendingDocumentationSection = section;
            $scope.pendingDocumentationNavigation = true;
            $location.path(path).search({}).hash(null);

            if (sameDocument) {
                $timeout($scope.scrollDocumentation, 0);
            }
        };

        $scope.scrollDocumentation = function () {
            var pane = document.querySelector(".article");
            var section = $scope.pendingDocumentationSection;
            var target = section ? document.getElementById(section) : null;

            if (!pane) {
                return;
            }

            if (target) {
                pane.scrollTop += target.getBoundingClientRect().top -
                    pane.getBoundingClientRect().top;
            } else if (!section) {
                pane.scrollTop = 0;
            }

            $scope.pendingDocumentationSection = null;
            $scope.pendingDocumentationNavigation = false;
        };

        $scope.$on("$viewContentLoaded", function () {
            if ($scope.pendingDocumentationNavigation) {
                $timeout($scope.scrollDocumentation, 0);
            }
        });

    });

document.addEventListener("toggle", function (event) {
    var element = event.target;
    var sidebar = element.closest(".nav");
    if (element instanceof HTMLDetailsElement && element.open &&
            element.hasAttribute("data-sidebar-accordion") && sidebar) {
        sidebar.querySelectorAll(
            "details[data-sidebar-accordion][open]"
        ).forEach(function (other) {
            if (other !== element && !other.contains(element) &&
                    !element.contains(other)) {
                other.open = false;
            }
        });
    }
}, true);
