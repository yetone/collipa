$(function() {
  var $hidden = $('.hidden');
  $D.on('mouseover', '.item', function() {
    $(this).find('.hidden').css('display', 'inline');
  }).on('mouseout', '.item', function () {
    $(this).find('.hidden').css('display', 'none');
  });

  $('#more-content').toggle(
    function() {
      var $this = $(this);
      $this.attr('title', '隐藏主题内容');
      $this.find('i').addClass('icon-chevron-up').removeClass('icon-chevron-down');
      if ($hidden.css('display') == 'none') {
        $hidden.slideDown(150);
      }
    },
    function() {
      var $this = $(this);
      $this.attr('title', '查看主题内容');
      $this.find('i').addClass('icon-chevron-down').removeClass('icon-chevron-up');
      if ($hidden.css('display') == 'block') {
        $hidden.slideUp(150);
      }
    }
  );

  $D.on('click', '.vote li a', function(e) {
    e.preventDefault();
    var $this = $(this),
        content = $this.html(),
        content_top = content.substr(0, content.indexOf('</i>') + 4),
        content_tail = content.substr(content.indexOf('</i>') + 5, content.length),
        count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')'))),
        url = $this.attr('href');

    if ($this.hasClass('disabled')) {
      return;
    }

    if ($this.parent('li').hasClass('edit')) {
      window.location.href = url;
      return;
    }

    if ($this.parent('li').hasClass('more')) {
      var $more = $this.parents('.more'),
          $more_list = $more.find('.menu-list');
      if ($more_list.hasClass('open')) {
        $more_list.removeClass('open');
      } else {
        $more_list.addClass('open');
      }
      return;
    }

    $this.addClass('disabled');
    $.ajax({
      url: url,
      type: 'PUT',
      data: {'_xsrf': get_cookie('_xsrf')},
      success: function(data) {
        if (data.status !== 'success') {
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
        $this.reoveClass('disabled');
      }
    });
  });
});
