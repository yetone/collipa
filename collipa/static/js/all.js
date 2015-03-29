/**
 * Created by yetone on 7/27/14.
 * all page run this js
 */

$(function() {
  $('.body-nav').fix();
  $('.nav-wrap .nav li').navBottomPosition();

  $.Collipa.shapeResize();

  $W.resize(function() {
    if ($('#head > .menu.fixed').length) {
      $.Collipa.shapeResize(true);
    } else {
      $.Collipa.shapeResize();
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

  function imagePreviewHandler() {
    var $imagePreviewWrap = $('.upload-popout .image-preview-wrap'),
        $imagePreview = $imagePreviewWrap.find('.image-preview'),
        $imgs = $imagePreview.find('img'),
        width;
    $imgs.load(function() {
      width = 0;
      $imgs.each(function(i, e) {
        var $e = $(e);
        width += $e.width() + parseInt($e.css('margin-right'));
        if (i === $imgs.length - 1) {
          $imagePreview.width(width + 2);
        }
      });

    })
  }

  $('#global-pic-select').imageUpload({
    cbk: function(_data) {
      var $imagePreview = $('.upload-popout .image-preview'),
          source = $('#upload-tpl').html(),
          render = template.compile(source);
      if ($imagePreview.length) {
        $imagePreview.append('<img data-id="' + _data.id + '" src="' + _data.path + '">');
        imagePreviewHandler();
        return;
      }
      $.ajax({
        url: '/album/list',
        type: 'GET'
      }).done(function(jsn) {
        var html;
        var data = {};
        data.image = _data;
        data.data = jsn.data;
        html = render(data);
        $.Collipa.popout({
          html: html,
          cbk: function() {
            imagePreviewHandler();
            initChosen();
          },
          ok: function(opt) {
            var $select = $('.album-select select'),
                $images = $('.upload-popout .image-preview img'),
                album_id = $select.val();
            $images.each(function(i) {
              var $e = $(this),
                  image_id = $e.data('id');
              $.ajax({
                url: '/image/' + image_id,
                type: 'PUT',
                data: {
                  album_id: album_id
                }
              }).done(function(jsn) {
                if (jsn.status !== 'success') {
                  return noty(jsn);
                }
                if (i === $images.length - 1) {
                  opt.cbk();
                }
              });
            });
          }
        })
      })
    }
  });

  function initChosen() {
    var $select = $('.album-select select'),
        id = $select.attr('id');
    $select.removeClass('chzn-done').removeAttr('id');
    $('#' + id + '_chzn').remove();
    $select.chosen({width: '145px', no_results_text: '没有专辑'});
  }

  function createAlbum() {
    var $input = $('input.album-create'),
        $btn = $('.album-create-btn'),
        name = $input.val();
    if ($btn.hasClass('sending')) {
      return;
    }
    $btn.addClass('sending').text('正在创建..');
    $.ajax({
      url: '/album/create',
      type: 'POST',
      dataType: 'json',
      data: {
        name: name
      },
      success: function(jsn) {
        $btn.removeClass('sending').text('创建');
        if (jsn.status !== 'success') {
          return noty(jsn);
        }
        $input.val('');
        var $select = $('.album-select select'),
            $selected = $select.find('option[selected]'),
            $opt = $('<option selected value="' + jsn.data.id + '">' + jsn.data.name + '</option>');
        $selected.removeAttr('selected');
        $select.prepend($opt);
        initChosen();
      }
    });
  }
  $D.on('keyup', 'input.album-create', function(e) {
    // 回车
    if (e.keyCode === 13) {
      e.preventDefault();
      createAlbum();
    }
  });

  $D.on('click', '.album-create-btn', function(e) {
    e.preventDefault();
    createAlbum();
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
