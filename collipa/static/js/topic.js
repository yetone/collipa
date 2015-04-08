$(function() {
  $('.nav-wrap li a, .pagination li a').pjax({
    container: '.reply-list',
    part: '.reply-list',
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
      SyntaxHighlighter.all();
    }
  });
  $D.on('mouseover', '.item', function() {
    $(this).find('.hidden').css('display', 'inline');
  }).on('mouseout', '.item', function () {
    $(this).find('.hidden').css('display', 'none');
  });

  $D.on('click', '.vote li a', function(e) {
    e.preventDefault();
    var $this = $(this),
        url = $this.attr('href'),
        content = $this.html(),
        content_top = content.substr(0, content.indexOf('</i>') + 4),
        content_tail = content.substr(content.indexOf('</i>') + 5, content.length),
        count = parseInt(content.substr(content.indexOf('(') + 1, content.indexOf(')')));

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
        $this.addClass('dn');
      }
      return;
    }

    if ($this.parent('li').hasClass('remove')) {
      return;
    }

    $this.addClass('disabled');
    $.ajax({
      url: url,
      type: 'PUT',
      data: {'_xsrf': get_cookie('_xsrf')},
      success: function(data) {
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
        $this.removeClass('disabled');
      }
    });
  });

  $D.on('click', '.reply-list .action .reply a', function(e) {
    e.preventDefault();
    var $this = $(this),
        $name_area = $this.parents('.item').find('a.name'),
        name = $name_area.attr('data-name'),
        nickname = $name_area.html(),
        user_url = $name_area.attr('href'),
        $textarea = $('#ueditor_0').contents().find('body');

    $textarea.focus();
    ue.execCommand('inserthtml', '@' + nickname + '&nbsp;');
  });

  $D.on('click', '.topic .action .reply a', function(e) {
    e.preventDefault();
    var top = $('#editor').offset().top;
    $("html, body").animate({scrollTop: top}, 500);
    ue.focus();
  });

  $D.on('click', '.reply-create button', function(e) {
    e.preventDefault();
    var $this = $(this),
        topic_id = $this.attr('data-id'),
        url = '/reply/create?topic_id=' + topic_id,
        $textarea = $('#ueditor_0').contents().find('body'),
        xsrf = get_cookie('_xsrf'),
        content = ue.getContent(),
        args = {"content": content, "_xsrf": xsrf};

    $this.attr('disabled', 'disabled').addClass('onloading').html("正在发布...");
    $.post(url, $.param(args), function(data) {
      $this.removeAttr('disabled').removeClass('onloading').html("发布");
      if (data.status !== 'success') {
        noty(data);
      } else {
        var source = $('#reply-template').html(),
            render = template.compile(source),
            html = render(data),
            $explain = $('.reply-list .explain');

        if ($explain.length > 0) {
          $explain.remove();
          $('.reply-list').append('<ul class="item-list"></ul>');
        }
        var $items = $('ul.item-list');
        $items.append(html);
        var $show = $('#show-' + data.id);
        $show.hide().fadeIn();

        $textarea.html('');
        SyntaxHighlighter.all();
      }
    });
  });

  $D.on('click', '.edui-for-myinsertimage', function(e) {
    e.preventDefault();
    $('#pic-select').click();
  });
  $('#pic-select').fileupload({
    url: '/image/upload?_xsrf=' + get_cookie('_xsrf'),
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10),
          status_msg = $('.status-msg');
      status_msg.addClass('loader-bar').html('图片上传进度：' + progress + '%');
      if (progress == 100) {
        status_msg.removeClass('loader-bar').html('图片上传完毕');
        setTimeout(function() {status_msg.html('');}, 500);
      }
    },
    done: function(e, result) {
      var status_msg = $('.status-msg'),
          waterfall = $('#post-page-waterfall'),
          post_id = $('#post_id').val(),
          data = result.result;

      if (data.status === "success") {
        data = data.data;
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-reply-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });

  // 删除操作
  (function() {
    var $remove = $('.remove a');
    $D.on('click', '.remove a', function(e) {
      e.preventDefault();
      var $this = $(this);
      $.Collipa.request({
        content: '确定删除？',
        ok: function(obj) {
          $('#remove-form').mySubmit({
            url: $this.attr('href'),
            success: function(jsn) {
              noty(jsn);
              obj.cbk();
              if ($this.parents('.reply-list').length) {
                $this.parents('li.item').animate({opacity: 0}, 500, function() {
                  $(this).remove();
                });
              } else {
                // window.location.href = '/';
              }
            }
          });
        }
      });
    });
  })();

  ue.addListener('ready', function() {
    ueReady();
  });

});
