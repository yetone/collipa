$(function() {
  var editorEmpty = function() {
    var $placeholder = $('<div class="tweet-placeholder">输入内容吧...</div>');
    $('.tweet-editor').html($placeholder)
                      .css({
                        'min-height': 19
                      });
  };
  $D.on('keyup', '.tweet-editor', function() {
    var $this = $(this),
        $btn = $('.tweet-submmit'),
        text = $this.text();
    if (text.length >= 3) {
      $btn.removeAttr('disabled');
    } else {
      $btn.attr('disabled', 'disabled');
    }
  });
  $D.on('focus', '.tweet-editor', function() {
    $('.tweet-placeholder').remove();
    $(this).css({
      'min-height': 60
    });
  });
  $D.on('blur', '.tweet-editor', function() {
    var $this = $(this),
        text = $.trim($this.text());
    if (!text.length) {
      editorEmpty();
    }
  });
  $D.on('keypress', '.tweet-editor', function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      $('.tweet-submmit').click();
      $(this).blur();
    }
  });
  $D.on('click', '.tweet-submmit', function() {
    var $this = $(this),
        $editor = $('.tweet-editor'),
        $btn = $('.tweet-submmit'),
        $tweetList = $('.tweet-list .item-list'),
        content = $editor.html(),
        text = $.trim($editor.text()),
        url = '/tweet/create';
    if (text.length) {
      $btn.attr('disabled', 'disabled');
      $.ajax({
        url: url,
        type: 'post',
        data: {
          content: content,
          '_xsrf': get_cookie('_xsrf')
        },
        success: function(data) {
          if (data.status === 'success') {
            var source = $('#tweet-template').html(),
                render = template.compile(source),
                html = render(data);
            $tweetList.prepend(html);
            editorEmpty();
            $('#show-' + data.id).css({
                                   opacity: 0
                                 })
                                 .animate({
                                   opacity: 1
                                 });
          } else {
            $btn.removeAttr('disabled');
            noty(data);
          }
        }
      });
    }
  });
});
