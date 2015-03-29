$(function() {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function() {};

  var WS = (function(undefined) {
    function WS() {
      this.handlers = {};
      this.connect();
    }

    var proto = WS.prototype;

    proto.connect = function() {
      var self = this;
      var url = "ws://" + window.location.host + "/api/websocket";

      self._socket = new WebSocket(url);
      self._socket.onopen = function(event) {
        console.log("::::::::websocket start::::::::");
      };
      self._socket.onmessage = function(event) {
        var body = JSON.parse(event.data);
        self.emit(body.event, body.data);
      };
      self._socket.onclose = function(event) {
        console.log("::::::::websocket close::::::::");
        setTimeout(self.connect.bind(self), 5000);
      };
    };

    proto.on = function(event, handler) {
      if (!this.handlers[event]) {
        this.handlers[event] = []
      }
      this.handlers[event].push(handler);

      return this;
    };

    proto.emit = function(event) {
      var handlers = this.handlers[event];
      var args = Array.prototype.slice.call(arguments, 1);
      if (!handlers || !handlers.length) return;

      for (var i = 0, l = handlers.length; i < l; i++) {
        var handler = handlers[i];
        handler.apply(handler, args);
      }

      return this;
    };

    return WS;
  })();

  var payloadHandlers = {
    $onlineCountArea: $('#footer #online-count'),
    $messageCountArea: $('#head .menu .message'),
    $notificationCountArea: $('#head .menu .notification'),
    $messageBoxArea: $('.organ.message-box'),

    handle: function() {
      var ws = new WS();
      ws.on('online', this.onlineHandler.bind(this))
        .on('message', this.messageHandler.bind(this))
        .on('notification', this.notificationHandler.bind(this));
    },

    onlineHandler: function(data) {
      if (!this.$onlineCountArea.length) return;
      this.$onlineCountArea.html(data.count + " 人在线");
    },

    notificationHandler: function(data) {
      if (+data.count === 0) return;
      if (this.$notificationCountArea.find('span.count').length) {
        this.$notificationCountArea.find('span.count').html(data.count);
      } else {
        this.$notificationCountArea.append('<span class="count">' + data.count + '</span>');
      }
      var $title = $('title');
      if ($title.html().indexOf('(新提醒)') === -1) {
        $title.html('(新提醒) ' + $title.html());
      }
    },

    messageHandler: function(data) {
      console.log("message");
      var $title = $('title');
      if (this.$messageBoxArea.attr('data-id') != data.message_box_id) {
        if (this.$messageCountArea.find('span.count').length) {
          this.$messageCountArea.find('span.count').html(data.count);
        } else {
          this.$messageCountArea.append('<span class="count">' + data.count + '</span>');
        }
        if ($title.html().indexOf('(新私信)') === -1) {
          $title.html('(新私信) ' + $title.html());
        }
      } else {
        var source = $('#message-tpl').html();

        var render = template.compile(source);
        var html = render(data);

        this.$messageBoxArea.find('ul.message-list').append(html);
        $.post(window.location.href + '&action=read');
      }
      var last_notify = window.localStorage.getItem("last_notify");
      if (last_notify != data.id) {
        window.localStorage.setItem("last_notify", data.id);
        notify.createNotification("新私信 from " + data.nickname + " - Collipa", {body: data.content, icon: data.avatar, url: "/messages?user_id=" + data.sender_id});
      }
    }
  };

  payloadHandlers.handle();
});
