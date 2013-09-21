// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    online.start();
});

var online = {
    socket: null,
    count_area: $('#footer #online-count'),

    start: function() {
      var url = "ws://" + location.host + "/api/getonlinecount";
      online.socket = new WebSocket(url);
      online.socket.onmessage = function(event) {
        console.log("is:::::")
        console.log(event);
        online.show_count(JSON.parse(event.data));
      }
      console.log("start");
    },

    show_count: function(count) {
      console.log(count);
      online.count_area.html(count + " 人在线");
    }
};
