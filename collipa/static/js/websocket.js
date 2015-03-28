$(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    online.start();
});

var online = {
    url: "ws://" + window.location.host + "/api/websocket",
    socket: null,
    onlineCountArea: $('#footer #online-count'),
    messageCountArea: $('#head .menu .message'),
    notificationCountArea: $('#head .menu .notification'),
    messageBoxArea: $('.organ.message-box'),

    start: function() {
      var self = this;
      self.socket = new WebSocket(self.url);
      self.socket.onopen = function(event) {
        console.log("::::::::websocket start::::::::");
      };
      self.socket.onmessage = function(event) {
        self.payloadHandler(JSON.parse(event.data));
      };
      self.socket.onclose = function(event) {
        console.log("::::::::websocket close::::::::");
        self.start();
      };
    },

    payloadHandler: function(data) {
      switch (data.type) {
        case 'online':
          this.onlineHandler(data);
          break;
        case 'message':
          this.messageHandler(data);
          break;
        case 'notification':
          this.notificationHandler(data);
          break;
        default:
          return;
      }
    },

    onlineHandler: function(data) {
      if (!this.onlineCountArea.length) return;
      this.onlineCountArea.html(data.count + " 人在线");
    },

    notificationHandler: function(data) {
      if (this.notificationCountArea.find('span.count').length) {
        this.notificationCountArea.find('span.count').html(data.count);
      } else {
        this.notificationCountArea.append('<span class="count">' + data.count + '</span>');
      }
      var title = $('title');
      if (title.html().indexOf('(新提醒)') === -1) {
        title.html('(新提醒) ' + title.html());
      }
    },

    messageHandler: function(data) {
      console.log("message");
      var $title = $('title');
      if (this.messageBoxArea.attr('data-id') != data.message_box_id) {
        if (this.messageCountArea.find('span.count').length) {
          this.messageCountArea.find('span.count').html(data.count);
        } else {
          this.messageCountArea.append('<span class="count">' + data.count + '</span>');
        }
        if ($title.html().indexOf('(新私信)') === -1) {
          $title.html('(新私信) ' + $title.html());
        }
      } else {
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

        this.messageBoxArea.find('ul.message-list').append(html);
        $.get(window.location.href + '&action=read');
      }
      var last_notify = window.localStorage.getItem("last_notify");
      if (last_notify != data.id) {
        window.localStorage.setItem("last_notify", data.id);
        var notification = notify.createNotification("新私信 from " + data.nickname + " - Collipa", {body: data.content, icon: data.avatar, url: "/messages?user_id=" + data.sender_id});
      }
    }
};
