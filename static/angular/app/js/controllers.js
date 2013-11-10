'use strict';

/* Controllers */

angular.module('collipa.controllers', []).
  controller('IndexCtrl', ['$scope', '$routeParams', 'Index', function($scope, $routeParams, Topic) {
    $scope.topics = Index.get({category: $routeParams.category});

  }])
  .controller('MyCtrl2', [function() {

  }]);
