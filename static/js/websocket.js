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
    online_count_area: $('#footer #online-count'),
    message_count_area: $('#head .menu .message'),
    message_box_area: $('.organ.message-box'),

    start: function() {
      var url = "ws://" + location.host + "/api/websocket";
      online.socket = new WebSocket(url);
      online.socket.onmessage = function(event) {
        console.log("::::::websocket::::::");
        online.show_message(JSON.parse(event.data));
      };
      online.socket.onclose = function(event) {
        console.log("::::::websocket close::::::");
        online.socket = new WebSocket(url);
      };
      console.log("::::::websocket start::::::");
    },

    show_message: function(data) {
      if (data.type === "online" && online.online_count_area.length) {
        online.online_count_area.html(data.count + " 人在线");
      } else if (data.type === "message") {
        console.log("okkkkkkkkkkkkk");
        if ((!online.message_box_area.length || online.message_box_area.attr('data-id') != data.message_box_id) && online.message_count_area.length) {
          if (online.message_count_area.find('span.count').length) {
            online.message_count_area.find('span.count').html(data.count);
          } else {
            online.message_count_area.append('<span class="count">' + data.count + '</span>');
          }
        } else if (online.message_box_area.length && online.message_box_area.attr('data-id') == data.message_box_id) {
          var source =
              '<li id="show-<%= id %>" data-id="<%= id %>" class="item message clearfix you">'
          +     '<a class="avatar" href="<%= url %>">'
          +       '<img class="avatar" src="<%= avatar %>">'
          +     '</a>'
          +     '<div class="item-content">'
          +       '<div class="meta">'
          +         '<span class="time"><%= created %></span>'
          +       '</div>'
          +       '<div class="content">'
          +         '<%= content %>'
          +         '<div class="caret">'
          +           '<div class="caret-outer"></div>'
          +           '<div class="caret-inner"></div>'
          +         '</div>'
          +       '</div>'
          +     '</div>'
          +   '</li>';

          var render = template.compile(source);
          var html = render(data);

          online.message_box_area.find('ul.message-list').append(html);
        }
      }
    }
};
