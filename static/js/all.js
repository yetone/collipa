/**
 * Created by yetone on 7/27/14.
 * all page run this js
 */

$(function() {
  $('.body-nav').fix();
  $('.nav-wrap .nav li').navBottomPosition();

  $.Collipa.shape_resize();

  $W.resize(function() {
    if ($('#head > .menu.fixed').length) {
      $.Collipa.shape_resize(true);
    } else {
      $.Collipa.shape_resize();
    }
  });

  $D.on('click', '.layout-close', function(e) {
    e.preventDefault();
    $('#layout').fadeOut();
    $.Collipa.removeBg();
  });

  $D.on('keypress', function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      $('form button').click();
    }
  });

  $D.click(function() {
    var $d = $('#noty.static');
    $d.fadeOut(1200);
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

  $D.on('mouseover', '.add-sth', function(e) {
    clearTimeout(G.addMenuTimer);
    e.preventDefault();
    var $this = $(this),
      $menu = $this.find('.min-menu');
    G.addMenuTimer = window.setTimeout(function() {
      $menu.removeClass('dn');
    }, 100);
  });

  $D.on('mouseout', '.add-sth', function(e) {
    clearTimeout(G.addMenuTimer);
    e.preventDefault();
    var $this = $(this),
      $menu = $this.find('.min-menu');
    G.addMenuTimer = window.setTimeout(function() {
      $menu.addClass('dn');
    }, 300);
  });

  $('#global-pic-select').imageUpload({
    cbk: function(data) {
      var source = $('#upload-tpl').html(),
          render = template.compile(source),
          html = render(data);
      $.Collipa.popout({
        ok: function(opt) {
          opt.cbk();
        },
      })
    }
  });

  $D.on('click', '.min-add-image', function(e) {
    e.preventDefault();
    $('#global-pic-select').click();
  });

  function Notifier() {
  }
  Notifier.prototype.notify = function(title, options) {
    var n;
    if (window.webkitNotifications) {
      n = window.webkitNotifications.createNotification(options.icon, title, options.body);
      n.onclick = function() {
        window.focus();
        this.cancel();
      };
      n.show();
    } else if (navigator.mozNotification) {
    }
  };
  notifier = new Notifier();

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
