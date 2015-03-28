$(function() {
  $D.on('click', '.profile-action a:first', function(e) {
    e.preventDefault();
    var $this = $(this),
        url = $this.attr('data-href'),
        $info_follow_area = $this.parents('.profile-head').find('.status li:last a span'),
        count = parseInt($info_follow_area.html());

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        $this.removeClass('onloading');
        if (data.type === 1) {
          $this.removeClass('fo').addClass('unfo');
          $this.html('已关注');
          count += 1;
        } else if (data.type === 0) {
          $this.removeClass('unfo').addClass('fo');
          $this.html('关注');
          count -= 1;
        }
        $info_follow_area.html(count);
      }
    });
    $this.addClass('onloading');
    button_content = $this.html();
    $this.html(button_content + ' ..');
  });

  $D.on('click', '.vote li a', function(e) {
    e.preventDefault();
    var $this = $(this),
        url = $this.attr('href'),
        content = $this.html(),
        content_top = content.substr(0, content.indexOf('</i>') + 4),
        content_tail = content.substr(content.indexOf('</i>') + 5, content.length),
        count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));

    if ($this.parent('li').hasClass('edit')) {
      window.location.href = url;
      return;
    }
    $.get(url, function(data) {
      if (data.status != 'success') {
        noty(data);
      } else {
        if (data.type === 1) {
          $this.parent('li').removeClass('pressed').addClass('pressed');
          content = content_top + ' 已' + content_tail;
          if (count > -1) {
            count += 1;
            content_top = content.substr(0, content.indexOf('('));
            content = content_top + '(' + count + ')';
          }
          $this.html(content);
          repel($this);
        } else if (data.type === 0) {
          $this.parent('li').removeClass('pressed');
          content_tail = content.substr(content.indexOf('已') + 1, content.length);
          content = content_top + ' ' + content_tail;
          if (count > -1) {
            count -= 1;
            if (data.category === 'up') {
              content = content_top + ' 赞同(' + count + ')';
            } else if (data.category === 'down') {
              content = content_top + ' 反对(' + count + ')';
            }
          }
          $this.html(content);
        }
      }
    });
  });

  $D.on('click', '.profile-action .mail', function(e) {
    e.preventDefault();
    var $this = $(this),
        $layout = $('#layout'),
        action = $this.attr('data-href'),
        source = $('#action-template').html(),
        render = template.compile(source),
        html = render({action: action});

    $layout.remove();
    $('body').append(html);
    $layout = $('#layout');
    $layout.popslide({
      cbk: function() {
        $('#layout.message textarea').focus();
      }
    });
  });

  $D.on('click', '#layout.message button', function(e) {
    e.preventDefault();
    var $this = $(this),
        $layout = $this.parents('#layout'),
        $form = $layout.find('form'),
        action = $form.attr('action'),
        $textarea = $form.find('textarea'),
        content = $textarea.val(),
        args = {'content': content, '_xsrf': get_cookie('_xsrf')};

    $this.attr('disabled', 'disabled').addClass('onloading').html("发送中...");
    $.post(action, $.param(args), function(data) {
      $this.removeAttr('disabled').removeClass('onloading').html("发送");
      if (data.status === 'success') {
        $layout.fadeOut();
        $.Collipa.removeBg();
        noty(data);

        $textarea.val('');
      } else {
        noty(data);
      }
    });
  });

  $D.on('click', '.message-fm button', function(e) {
    e.preventDefault();
    var $this = $(this),
        $form = $this.parents('form'),
        $textarea = $form.find('textarea'),
        action = $form.attr('action'),
        content = $textarea.val(),
        $items = $this.parents('.message-fm').prev('ul'),
        args = {'content': content, '_xsrf': get_cookie('_xsrf')};

    $this.attr('disabled', 'disabled').addClass('onloading').html("发送中...");
    $.post(action, $.param(args), function(data) {
      $this.removeAttr('disabled').removeClass("onloading").html("发送");
      if (data.status === 'success') {
        var source = $('#message-template').html(),
            render = template.compile(source),
            html = render(data);

        $items.append(html);
        var $show = $('#show-' + data.id);
        $show.hide().fadeIn();

        $textarea.val('');
      } else {
        noty(data);
      }
    });
  });

  $D.on('click', '.more > a', function(e) {
    e.preventDefault();
    var $more = $(this).parents('.more'),
        $more_list = $more.find('.menu-list');
    if ($more_list.hasClass('open')) {
      $more_list.removeClass('open');
    } else {
      $more_list.addClass('open');
    }
  });

  $D.on('click', '.nav-wrap li', function() {
    var $this = $(this);
    $this.siblings().removeClass('on');
    $this.addClass('on');
  });
  $('.nav-wrap li a, .pagination li a').pjax({
    container: '#pjax-content',
    part: '#pjax-content',
    success: function() {
      var $no = $('.nav-wrap li.on'),
          $nbs;
      if ($no.length) {
        $nbs = $no.parents('.nav-wrap').find('.nav-bottom-span');
        setTimeout(function() {
          $no.trigger('mouseover');
          if ($nbs.length) {
            $nbs.css({'opacity': 1});
          }
        }, 300);
      }
    }
  });
});
