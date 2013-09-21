var repel = function(data) {
  if (data.parent('li').hasClass('up')) {
    var buff = '.down a';
  } else if (data.parent('li').hasClass('down')) {
    var buff = '.up a';
  } else {
    return false;
  }
  var $that = data.parents('ul.vote').find(buff);
  var content = $that.html();
  var content_top = content.substr(0, content.indexOf('</i>') + 4);
  var content_tail = content.substr(content.indexOf('</i>') + 5, content.length);
  var count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));
  if (content.indexOf('已') !== -1) {
    $that.parent('li').removeClass('pressed');
    content_tail = content.substr(content.indexOf('已') + 1, content.length)
    content = content_top + ' ' + content_tail;
    if (count > -1) {
      count -= 1;
      content_top = content.substr(0, content.indexOf('('));
      content = content_top + "(" + count + ")";
    }
    $that.html(content);
  }
};

$(function () {
  $('.profile-action a:first').live('click', function() {
    var url = $(this).attr('href');
    var $info_follow_area = $(this).parents('.profile-head').find('.status li:last a span');
    var count = parseInt($info_follow_area.html());
    var $that = $(this);

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        $that.removeClass('onloading');
        if (data.type === 1) {
          $that.removeClass('fo').addClass('unfo');
          $that.html('已关注');
          count += 1;
        } else if (data.type === 0) {
          $that.removeClass('unfo').addClass('fo');
          $that.html('关注');
          count -= 1;
        }
        $info_follow_area.html(count);
      }
    });
    $that.addClass('onloading');
    button_content = $that.html();
    $that.html(button_content + ' ..');
    return false;
  });

  $('.vote li a').live('click', function() {
    var url = $(this).attr('href');
    if ($(this).parent('li').hasClass('edit')) {
      window.location.href = url;
      return;
    }
    var content = $(this).html();
    var content_top = content.substr(0, content.indexOf('</i>') + 4);
    var content_tail = content.substr(content.indexOf('</i>') + 5, content.length);
    var count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));
    var $that = $(this);
    $.get(url, function(data) {
      if (data.status != 'success') {
        noty(data);
      } else {
        if (data.type === 1) {
          $that.parent('li').removeClass('pressed').addClass('pressed');
          content = content_top + ' 已' + content_tail;
          if (count > -1) {
            count += 1;
            content_top = content.substr(0, content.indexOf('('));
            content = content_top + '(' + count + ')';
          }
          $that.html(content);
          repel($that);
        } else if (data.type === 0) {
          $that.parent('li').removeClass('pressed');
          content_tail = content.substr(content.indexOf('已') + 1, content.length)
          content = content_top + ' ' + content_tail;
          if (count > -1) {
            count -= 1;
            if (data.category === 'up') {
              content = content_top + ' 赞同(' + count + ')';
            } else if (data.category === 'down') {
              content = content_top + ' 反对(' + count + ')';
            }
          }
          $that.html(content);
        }
      }
    });
    return false;
  });

  $('.more > a').live('click', function() {
    var $more = $(this).parents('.more');
    var $more_list = $more.find('.menu-list');
    if ($more_list.hasClass('open')) {
      $more_list.removeClass('open');
    } else {
      $more_list.addClass('open');
    }
    return false;
  });
  $(document).click(function() {
    var $d = $('.open.menu-list');
    $d.removeClass('open');
  });
});
