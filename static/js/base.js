var superLove = function() {
  console.log("\n%c  ", "font-size:220px; background:url(http://collipa.com/static/upload/image/2013/12/1388025973qfHmWn_1.jpg) no-repeat 0px 0px;");

  return "You are my love."
}

var get_cookie = function(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r?r[1]:undefined;
  },

  mousePosition = function(e) {
    if (e.pageX && e.pageY) {
      return {x: e.pageX, y: e.pageY};
    }
    return {
      x: e.clientX + document.body.scrollLeft - document.body.clientX,
      y: e.clientY + document.body.scrollTop - document.body.clientY
    };
  },

  popup = function($popdiv, pos) {
    if (!pos) {
      pos = 'absolute';
    }
    var _scrollHeight = $(document).scrollTop(),
        _windowHeight = $(window).height(),
        _windowWidth  = $(window).width(),
        _popdivHeight = $popdiv.height(),
        _popdivWidth  = $popdiv.width();

    _popTop = (_windowHeight - _popdivHeight) / 2;
    _popLeft = (_windowWidth - _popdivWidth) / 2;
    $popdiv.css({'left': _popLeft + 'px', 'top': _popTop + 'px', 'display': 'block', 'position': pos});
    if ($popdiv.width() + 2 >= _windowWidth) {
      $popdiv.width(_windowWidth * 0.85);
    }
  },

  repel = function(data) {
    var buff;
    if (data.parent('li').hasClass('up')) {
      buff = '.down a';
    } else if (data.parent('li').hasClass('down')) {
      buff = '.up a';
    } else {
      return false;
    }
    var $this = data.parents('ul.vote').find(buff);
    var content = $this.html(),
        content_top = content.substr(0, content.indexOf('</i>') + 4),
        content_tail = content.substr(content.indexOf('</i>') + 5, content.length),
        count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));

    if (content.indexOf('已') !== -1) {
      $this.parent('li').removeClass('pressed');
      content_tail = content.substr(content.indexOf('已') + 1, content.length);
      content = content_top + ' ' + content_tail;
      if (count > -1) {
        count -= 1;
        content_top = content.substr(0, content.indexOf('('));
        content = content_top + "(" + count + ")";
      }
      $this.html(content);
    }
  },

  $D = $(document),
  $W = $(window);

var noty = function(data, static) {
  var noty_div;
  if (!data) {
    noty_div =
      '<div id="noty" class="info">'
    +   "您操作过快，服务器未响应"
    + '</div>';
  } else if (data.status) {
    noty_div =
      '<div id="noty" class="' + data.status + '">'
    +   data.message
    + '</div>';
  }

  $('#noty').remove();
  $('body').append(noty_div);
  popup($('#noty'), 'fixed');
  if (!static) {
    setTimeout(function() {$('#noty').fadeOut(1200);}, 600);
  } else {
    $('#noty').addClass('static');
  }
};

var $body_nav = $('.body-nav');
if ($body_nav.length) {
  var nav_top = $body_nav.offset().top;
}

$(function() {
  var fix_nav_bar = function() {
    var top = $(document).scrollTop(),
        menu_top,
        $shape = $('#shape'),
        $nav = $('.body-nav'),
        $nav_fixed = $('.body-nav.fixed'),
        $menu = $('#head .menu'),
        $menu_fixed = $('#head .menu.fixed'),
        $head = $('#head');

    var nav_width = $nav.width(),
        nav_height = $nav.height(),
        menu_left = $menu.offset().left,
        menu_height = $menu.height(),
        head_left = $head.offset().left;

    if (top >= nav_top) {
      if (!$nav_fixed.length) {
        menu_top = (parseInt(nav_height) - parseInt(menu_height)) / 2;
        $nav_fixed = $nav.clone();
        $menu_fixed = $menu.clone();
        $nav_fixed.addClass('fixed').css({'width': nav_width});
        $nav.after($nav_fixed);
        $menu_fixed.addClass('fixed').css({'right': +head_left + 20 + 'px', 'top': menu_top + 'px'});
        $menu_fixed.insertAfter($menu).hide().fadeIn(600);
      }
    } else {
      $nav_fixed.remove();
      $menu_fixed.remove();
    }
  },
  shape_resize = function(data) {
    var window_height = $(window).height(),
        window_width = $(window).width(),
        shape_width = $('#shape').width();
    var min_width = window_width <= shape_width ? window_width : shape_width;

    if (window_width === min_width) {
      $('#shape').addClass('mobile').css({'width': window_width});
      var $imgs = $('.content img');
      $imgs.each(function() {
        if ($(this).width() > min_width) {
          $(this).css({"max-width": min_width - 20 + 'px'});
        }
      });
    } else {
      $('#shape').removeClass('mobile').css({'width': '720px'});
    }
    if (data) {
      var $head = $('#head'),
          $menu_fixed = $('#head > .menu.fixed'),
          $nav = $('.nav');
      var head_left = $head.offset().left;
      $nav.css({'width': min_width - 20 + 'px'});
      $menu_fixed.css({'right': +head_left + 20 + 'px'});
    }


  };


  fix_nav_bar();

  shape_resize();

  $(window).resize(function() {
    if ($('#head > .menu.fixed').length) {
      shape_resize(true);
    } else {
      shape_resize();
    }
  });

  $D.on('click', '.layout-close', function(e) {
    e.preventDefault();
    $('#layout').fadeOut();
  });

  $D.live('keypress', function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      $('form button').click();
    }
  });

  $D.click(function() {
    var $d = $('#noty.static');
    $d.fadeOut(1200);
  });

  $D.scroll(function() {
    if ($body_nav.length) {
      fix_nav_bar();
    }
  });

  if (notify.permissionLevel() === notify.PERMISSION_DEFAULT) {
    var html = '<div id="open-notification" class="tc"><a href="#;">点我开启桌面提醒</a></div>';
    $('body').prepend(html);
  }

  $D.on('click', '#open-notification a', function() {
    notify.requestPermission(function(){
      if (notify.permissionLevel() === notify.PERMISSION_GRANTED) {
        $('#open-notification').remove();
      }
    });
  });

  function notifier() {
  }
  notifier.prototype.notify = function(icon, title, message) {
      if (window.webkitNotifications !== undefined) {
        window.webkitNotifications.createNotification(icon, title, message).show();
      }
  };

  $.notifier = new notifier();

  $.fn.extend({
    tooltip: function() {
      this.each(function(i, v) {
        var $v = $(v);
        $v.off('mousemove').off('mouseout');
        $v.on('mousemove', function(e) {
          var text = $(v).attr('data-tooltip');
          if (!$('.tooltip').length) {
            var tooltip = '<div class="tooltip"></div>';
            $(tooltip).appendTo('body').fadeIn();
          }
          $('.tooltip').css({'position': 'absolute',
                             'top': mousePosition(e).y + 15,
                             'left': mousePosition(e).x + 15
          }).html(text);
        }).on('mouseout', function(e) {
          $('.tooltip').fadeOut(150);
          setTimeout(function() {$('.tooltip').remove();}, 150);
        });
      });
    }
  });

  $D.click(function() {
    var $d = $('.open.menu-list');
    $d.removeClass('open');
  });

  var cslMessage = "             ___    ___                            \n"+
                   "            /\\_ \\  /\\_ \\    __                     \n"+
                   "  ___    ___\\//\\ \\ \\//\\ \\  /\\_\\  _____      __     \n"+
                   " /'___\\ / __`\\\\ \\ \\  \\ \\ \\ \\/\\ \\/\\ '__`\\  /'__`\\   \n"+
                   "/\\ \\__//\\ \\L\\ \\\\_\\ \\_ \\_\\ \\_\\ \\ \\ \\ \\L\\ \\/\\ \\L\\.\\_ \n"+
                   "\\ \\____\\ \\____//\\____\\/\\____\\\\ \\_\\ \\ ,__/\\ \\__/.\\_\\\n"+
                   " \\/____/\\/___/ \\/____/\\/____/ \\/_/\\ \\ \\/  \\/__/\\/_/\n"+
                   "                                   \\ \\_\\           \n"+
                   "                                    \\/_/           \n"+
                   "\n联系方式：i@yetone.net";
  window.console && console.info && console.info(cslMessage);
});
