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

  $('.profile-action .mail').live('click', function() {
    var user_id = $(this).attr('data-uid');

    layout =
      '<div id="layout" class="message">'
    +   '<div class="layout-header">'
    +     '<div class="title">'
    +       '发送私信'
    +     '</div>'
    +     '<a title="关闭" class="layout-close">'
    +       '<i class="icon-remove"></i>'
    +     '</a>'
    +   '</div>'
    +   '<div class="layout-content">'
      +   '<form>'
      +     '<input type="hidden" name="_xsrf" value="' + get_cookie('_xsrf') + '">'
      +     '<div class="fm-row">'
      +       '<div class="fm-item">'
      +         '<textarea name="content"></textarea>'
      +       '</div>'
      +     '</div>'
      +     '<div class="fm-action">'
      +       '<button type="submit" class="btn message-submit" data-uid="' + user_id + '">发送</button>'
      +     '</div>'
      +   '</form>'
    +   '</div>'
    + '</div>';

    $('#layout').remove();
    $('body').append(layout);
    popup($('#layout'));
    $('#layout.message textarea').focus();

    return false;
  });

  $('button.message-submit').live('click', function() {
    new_message($(this));
    return false;
  });

  clp_message.start();
});

function new_message($this) {
  var user_id = $this.attr('data-uid');
  var $form = $this.parents('form');
  var $textarea = $form.find('textarea');
  var content = $textarea.val();
  clp_message.socket.send(content, user_id);
  $this.attr('disabled', 'disabled');
}

var clp_message = {
  socket: null,
  count_area: $('#head .message'),
  message_area: $('ul.message-list'),

  start: function() {
    var url = "ws://" + location.host + "/api/messagewebsocket";
    clp_message.socket = new WebSocket(url);
    clp_message.socket.onmessage = function(event) {
      clp_message.show_count(JSON.parse(event.data));
      if (clp_message.message_area.length) {
        clp_message.show_message(JSON.parse(event.data));
      }
    }
    console.log("start");
  },

  show_count: function(message) {
    $btn = $('.message-fm button');
    var $form = $this.parents('form');
    var $textarea = $form.find('textarea');
    var $layout = $btn.parents('#layout')
    $btn.removeAttr('disabled');
    if (data.status === 'success') {
      if ($layout.length) {
        $layout.fadeOut();
      }
      noty(data);

      $textarea.val('');
    } else {
      noty(data);
    }
  },

  show_message: function(data) {
    $btn = $('.message-fm button');
    $btn.removeAttr('disabled');
    var $form = $this.parents('form');
    var $textarea = $form.find('textarea');
    if (data.status === 'success') {
      var source =
          '<li id="show-<%= id %>" data-id="<%= id %>" class="item message clearfix me">'
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

      clp_message.show_message.append(html);
      var $show = $('#show-' + data.id);
      $show.hide().fadeIn();

      $textarea.val('');
    } else {
      noty(data);
    }
  }
};
