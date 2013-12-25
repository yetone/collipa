var love = function() {
  var loveMessage = "瓦日瓦瓦瓦毋瓦毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日日日日日瓦瓦瓦日\n"+
                    "瓦己日瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日日日日日日日日日日己己己己己己日毋瓦日\n"+
                    "瓦日瓦瓦瓦毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日瓦瓦瓦日\n"+
                    "瓦日瓦毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日瓦瓦瓦瓦瓦瓦瓦日日日日日瓦瓦瓦己\n"+
                    "瓦日瓦毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦日瓦瓦瓦日日日日日瓦瓦瓦瓦瓦日日瓦瓦瓦瓦瓦瓦日\n"+
                    "瓦瓦毋毋毋毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日瓦瓦日日瓦瓦瓦瓦瓦毋鬼毋\n"+
                    "瓦瓦毋毋毋毋毋毋毋毋毋瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦瓦日日日日日日日日瓦瓦瓦瓦毋鬼毋\n"+
                    "毋瓦毋毋毋毋毋毋毋毋瓦毋車馬馬鬼鬼鬼鬼毋瓦瓦瓦日日日日己日日日日瓦瓦瓦瓦日\n"+
                    "毋瓦毋毋毋毋毋毋瓦瓦車龠齱齱齱齱龍齱齱龍鬼日日日日己己己己日日日日日毋瓦己\n"+
                    "毋瓦毋毋毋毋毋瓦瓦鬼齱齱龍齱龍龍龍龍龍龍龍馬瓦日日己己己己己日日日日毋瓦日\n"+
                    "毋瓦毋毋毋毋瓦瓦鬼齱齱齱齱齱齱龍龍龍龍龍龍齱馬日己己己己乙己己日日己瓦日己\n"+
                    "毋瓦毋毋毋毋瓦車齱齱龍龍齱齱齱齱龍龠龍龍龍龍龍車己己己乙乙乙己己己己己乙十\n"+
                    "毋瓦毋毋毋毋毋龍齱齱齱齱齱齱齱龍龍馬龠龍龍龍龍龠瓦己乙乙乙乙乙己己己己己十\n"+
                    "毋瓦毋毋毋瓦鬼齱龍齱齱齱齱龍龍龠馬鬼鬼龠龍龍龠龠車乙乙乙乙乙乙乙己己日己乙\n"+
                    "毋瓦毋毋毋瓦馬齱龍齱齱龍馬車車毋毋毋車鬼龠龠龠馬車己乙乙十十乙乙乙乙己乙十\n"+
                    "毋瓦毋毋毋毋馬龍龍龍龍鬼毋毋毋毋毋毋毋毋鬼馬馬馬車己乙十十十乙乙乙乙乙乙亅\n"+
                    "瓦瓦毋毋毋毋龠齱龍龍鬼車毋毋毋毋毋毋瓦毋毋鬼馬鬼車己乙十十十十十十乙乙乙亅\n"+
                    "日日毋毋毋瓦馬齱龍龠車毋毋毋毋瓦瓦瓦瓦瓦毋車鬼鬼車己十十十十十十十十己己十\n"+
                    "己日毋毋毋瓦馬齱龍馬車車車毋瓦瓦瓦瓦瓦毋車車車車鬼日十十十十十十十十乙乙亅\n"+
                    "己己毋毋毋毋鬼齱龠鬼鬼鬼鬼鬼車毋毋毋車車車車車毋鬼日十十十十十十十十十亅丶\n"+
                    "乙己毋毋毋瓦車龍龠車車鬼鬼鬼車毋瓦毋車鬼鬼車毋毋車己十十十十十十亅十十十丶\n"+
                    "乙乙瓦毋毋毋毋馬馬車車鬼鬼鬼車瓦瓦毋毋車車毋瓦毋毋己乙十十十十十亅亅亅亅丶\n"+
                    "乙乙瓦毋毋毋瓦車鬼車毋毋毋毋瓦瓦瓦瓦瓦瓦日日瓦毋瓦己己乙乙十十亅亅亅亅亅丶\n"+
                    "乙乙瓦毋毋毋瓦毋鬼車毋毋瓦瓦瓦瓦日瓦日日己己日瓦日己己己乙十亅亅亅亅十亅丶\n"+
                    "乙乙日毋毋毋瓦瓦毋車毋毋瓦瓦瓦瓦日瓦瓦己己己日日乙己己己己乙亅亅亅亅十亅丶\n"+
                    "乙乙日毋毋毋毋瓦瓦毋車毋毋瓦毋毋毋毋瓦日己己日己乙乙乙乙己乙十亅亅亅亅亅　\n"+
                    "乙乙日毋毋毋瓦瓦瓦毋車毋毋毋毋毋瓦瓦瓦日日日日乙十乙乙乙乙乙十亅亅亅亅亅丶\n"+
                    "乙乙日瓦毋毋瓦瓦瓦瓦車車毋車車毋毋毋毋毋瓦瓦日乙十十十十十乙十亅亅亅亅亅丶\n"+
                    "乙乙瓦毋毋毋瓦瓦瓦瓦車車毋毋車車車車車瓦瓦毋日乙十十十十十十十十亅亅亅丶　\n"+
                    "己乙瓦毋毋毋瓦瓦瓦瓦鬼鬼車毋毋毋毋毋瓦瓦毋瓦己乙乙十亅亅亅亅十十亅亅十亅丶\n"+
                    "日己毋毋毋毋瓦瓦瓦瓦鬼鬼車毋瓦瓦瓦瓦瓦毋毋日己乙乙十亅亅亅亅十十十十乙十亅\n"+
                    "日日毋毋毋毋瓦瓦瓦瓦鬼鬼車車毋毋瓦瓦毋毋毋日己乙乙十亅亅亅亅亅十十十十十丶\n"+
                    "日瓦毋毋毋毋瓦瓦瓦日車車毋毋車車車車毋瓦毋瓦己乙乙十亅亅亅亅亅十十十十十亅\n"+
                    "己瓦毋毋毋毋瓦瓦瓦瓦車毋毋毋毋毋毋瓦瓦瓦毋毋瓦日乙十十亅亅亅亅亅十十乙十亅\n"+
                    "日毋車毋毋毋毋毋毋車車毋瓦瓦瓦瓦瓦日日瓦瓦瓦瓦瓦日日己乙十亅亅亅十十十十丶\n"+
                    "毋毋車車車鬼鬼車車車毋瓦瓦瓦日日日日日瓦瓦瓦瓦日日瓦日己己十亅亅亅十十十亅\n"+
                    "車毋車車車馬馬鬼車毋毋瓦瓦日日日日日日日日日日日日瓦日己己十亅亅亅亅乙乙十\n"+
                    "鬼車車車車車鬼馬車瓦瓦瓦日日日日日己己日日己日日瓦瓦日己己亅亅亅亅亅十十亅\n"+
                    "鬼車鬼車車毋毋鬼鬼毋日日日日己己己己己己己己己乙己乙乙十亅亅亅亅亅亅十乙亅\n"+
                    "鬼車鬼車車車毋毋瓦瓦日己己己乙乙乙乙乙乙乙乙乙乙十十十十亅亅亅亅亅亅乙十亅\n"+
                    "鬼毋車車車毋瓦日日己乙乙乙十十十十十十十亅亅亅亅亅亅亅丶丶丶丶丶丶丶丶丶　";
  console.log(loveMessage);
};

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
  }

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

});
