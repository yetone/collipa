'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('collipa.services', ['ngResource']).
  factory('Topic', ['$resource', function($resource) {
    return $resource('topic/:topicId.json', {}, {
      query: {method: 'GET', params: {topicId: 'topics'}, isArray: true}
    });
  }]).
  factory('Index', ['$resource', function($resource) {
    return $resource('index/:category.json', {}, {
      qurey: {method: 'GET', params: {category: 'index'}, isArray: true}
    });
  }]);
