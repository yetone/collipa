$(function() {
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

  $D.on('click', '.reply-list .action .reply a', function(e) {
    e.preventDefault();
    var $this = $(this),
        $name_area = $this.parents('.item').find('a.name'),
        name = $name_area.attr('data-name'),
        nickname = $name_area.html(),
        user_url = $name_area.attr('href'),
        $textarea = $('#ueditor_0').contents().find('body');

    $textarea.focus();
    ue.execCommand('inserthtml', '&nbsp;<a class="mention" data-username="' + name + '" href="'+ user_url +'">@' + nickname + '</a>&nbsp;');
  });

  $D.on('click', '.topic .action .reply a', function(e) {
    e.preventDefault();
    var top = $('#editor').offset().top;
    $("html, body").animate({scrollTop: top}, 500);
    ue.focus();
  });

  $D.on('click', '.reply-create button', function(e) {
    e.preventDefault();
    var $this = $(this);
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
        var source =
              '<li id="show-<%= id %>" data-id="<%= id %>" class="item clearfix">'
            +   '<a class="avatar fl" href="<%= author_url %>">'
            +     '<img class="avatar" src="<%= author_avatar %>">'
            +   '</a>'
            +   '<div class="item-content">'
            +     '<div class="author-info">'
            +       '<a class="name" data-name="<%= author_name %>"><%= author_nickname %></a>'
            +       '<span><%= floor %> 楼,</span>'
            +       '<a class="time" href="<%= reply_url %>"><%= created %></a>'
            +     '</div>'
            +   '<div class="content reply-content">'
            +     '<%== content %>'
            +   '</div>'
            +   '<div class="meta">'
            +     '<ul class="vote clearfix hidden">'
            +       '<li class="up">'
            +         '<a title="赞同" href="<%= reply_url %>?action=up">'
            +           '<i class="icon-thumbs-up"></i>'
            +           ' 赞同(0)'
            +         '</a>'
            +       '</li>'
            +       '<li class="down">'
            +         '<a title="反对" href="<%= reply_url %>?action=down">'
            +           '<i class="icon-thumbs-down"></i>'
            +           ' 反对(0)'
            +         '</a>'
            +       '</li>'
            +       '<li class="collect">'
            +         '<a title="收藏" href="<%= reply_url %>?action=collect">'
            +           '<i class="icon-bookmark"></i>'
            +           ' 收藏'
            +         '</a>'
            +       '</li>'
            +       '<li class="edit">'
            +         '<a title="修改" href="<%= reply_url %>/edit">'
            +           '<i class="icon-pencil"></i>'
            +           ' 修改'
            +         '</a>'
            +       '</li>'
            +     '</ul>'
            +     '<ul class="action clearfix">'
            +       '<li class="reply">'
            +         '<a title="回复" href="#;">'
            +           '<i class="icon-reply"></i>'
            +         '</a>'
            +       '</li>'
            +     '</ul>'
            +   '</div>'
            + '</li>',
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

  $D.on('click', '.more > a', function(e) {
    e.preventDefault();
    var $this = $(this),
        $more = $this.parents('.more'),
        $more_list = $more.find('.menu-list');

    if ($more_list.hasClass('open')) {
      $more_list.removeClass('open');
    } else {
      $more_list.addClass('open');
    }
  });
  $D.on('click', this, function() {
    var $d = $('.open.menu-list');
    $d.removeClass('open');
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
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-reply-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });

  ue.addListener('ready', function() {
    $('#ueditor_0').contents().find('body').keypress(function(e) {
      if (e.ctrlKey && e.which == 13 || e.which == 10) {
        $('.reply-create button').click();
      }
    });
  });
});
