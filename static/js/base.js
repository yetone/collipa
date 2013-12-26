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
  };

var noty = function(data, static) {
    if (!data) {
      var noty_div =
        '<div id="noty" class="info">'
      +   "您操作过快，服务器未响应"
      + '</div>';
    } else if (data.status) {
      var noty_div =
        '<div id="noty" class="' + data.status + '">'
      +   data.message
      + '</div>';
    }

    $('#noty').remove();
    $('body').append(noty_div);
    popup($('#noty'), 'fixed');
    if (!static) {
      setTimeout(function() {$('#noty').fadeOut(1200)}, 600);
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
    var top = $(document).scrollTop();
    var $shape = $('#shape');
    var $nav = $('.body-nav');
    var $nav_fixed = $('.body-nav.fixed');
    var $menu = $('#head .menu');
    var $menu_fixed = $('#head .menu.fixed');
    var $head = $('#head');
    var nav_width = $nav.width();
    var nav_height = $nav.height();
    var menu_left = $menu.offset().left;
    var menu_height = $menu.height();
    var head_left = $head.offset().left;

    if (top >= nav_top) {
      if (!$nav_fixed.length) {
        var menu_top = (parseInt(nav_height) - parseInt(menu_height)) / 2;
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
    var window_height = $(window).height();
    var window_width = $(window).width();
    var shape_width = $('#shape').width();
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
      var $head = $('#head');
      var $menu_fixed = $('#head > .menu.fixed');
      var $nav = $('.nav');
      var head_left = $head.offset().left;
      $nav.css({'width': min_width - 20 + 'px'});
      $menu_fixed.css({'right': +head_left + 20 + 'px'});
    }


  };


  fix_nav_bar();

  shape_resize();

  $(window).resize(function (){
    if ($('#head > .menu.fixed').length) {
      shape_resize(true);
    } else {
      shape_resize();
    }
  });

  $('.layout-close').live('click', function() {
    $('#layout').fadeOut();

    return false;
  });

  $(document).live('keypress', function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      $('form button').click();
    }
  });

  $(document).click(function() {
    var $d = $('#noty.static');
    $d.fadeOut(1200);
  });

  $(document).scroll(function() {
    if ($body_nav.length) {
      fix_nav_bar();
    }
  });

  if (notify.permissionLevel() === notify.PERMISSION_DEFAULT) {
    var html = '<div id="open-notification" class="tc"><a href="#;">点我开启桌面提醒</a></div>';
    $('body').prepend(html);
  }

  $('#open-notification a').on('click', this, function() {
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
        $(v).off('mousemove').off('mouseout');
        $(v).on('mousemove', function(e) {
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
  console.log(cslMessage);
});
