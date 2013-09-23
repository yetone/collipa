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
    t: null,
    online_count_area: $('#footer #online-count'),
    message_count_area: $('#head .menu .message'),
    notification_count_area: $('#head .menu .notification'),
    message_box_area: $('.organ.message-box'),

    start: function() {
      var url = "ws://" + location.host + "/api/websocket";
      online.create_socket(url);
      online.socket.onclose = function(event) {
        if (online.socket.readyState !== 1) {
          console.log("::::::::websocket close::::::::");
          clearInterval(online.t);
          online.t = setInterval(function() {online.create_socket(url)}, 1000);
        }
      };
    },

    create_socket: function(url) {
      online.socket = new WebSocket(url);
      online.socket.onmessage = function(event) {
        clearInterval(online.t);
        console.log("::::::::websocket start::::::::");
        online.show_message(JSON.parse(event.data));
      };
      console.log("::::::::websocket::::::::");
      online.socket.onclose = function(event) {
        if (online.socket.readyState !== 1) {
          console.log("::::::::websocket close::::::::");
          clearInterval(online.t);
          online.t = setInterval(function() {online.create_socket(url)}, 1000);
        }
      };
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
          try {
            online.fixed_message_count_area = $('#head .menu.fixed .message');
            if (online.fixed_message_count_area.find('span.count').length) {
              online.fixed_message_count_area.find('span.count').html(data.count);
            } else {
              online.fixed_message_count_area.append('<span class="count">' + data.count + '</span>');
            }
          } catch(e) {
            console.log("no fixed");
          }
          var title = $('title');
          if (title.html().indexOf('(新私信)') === -1) {
            title.html('(新私信) ' + title.html());
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
        var last_notify = window.localStorage.getItem("last_notify");
        if (last_notify != data.id) {
          window.localStorage.setItem("last_notify", data.id);
          notify.createNotification("新私信 from " + data.nickname + " - Collipa", {body: data.content, icon: data.avatar});
        }
      } else if (data.type === "notification") {
        if (online.notification_count_area.find('span.count').length) {
          online.notification_count_area.find('span.count').html(data.count);
        } else {
          online.notification_count_area.append('<span class="count">' + data.count + '</span>');
        }
        try {
          online.fixed_notification_count_area = $('#head .menu.fixed .notification');
          if (online.fixed_notification_count_area.find('span.count').length) {
            online.fixed_notification_count_area.find('span.count').html(data.count);
          } else {
            online.fixed_notification_count_area.append('<span class="count">' + data.count + '</span>');
          }
        } catch(e) {
          console.log("no fixed");
        }
        var title = $('title');
        if (title.html().indexOf('(新提醒)') === -1) {
          title.html('(新提醒) ' + title.html());
        }
      }
    }
};
