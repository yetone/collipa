$(function() {
  var $editor = $('.tweet-editor'),
      $toolbar = $('.tweet-box .toolbar'),
      $btn = $('.tweet-submit'),
      editorEmpty = function() {
        var $placeholder = $('<div class="tweet-placeholder">输入内容吧...</div>');
        $editor.stop(true, true);
        $editor.html($placeholder)
                          .animate({
                            'min-height': 19
                          }, 160);
        $toolbar.stop(true, true);
        $toolbar.fadeOut(160);
      },
      checkBtn = function() {
        var text = $editor.text();
        if (text.length >= 3) {
          $btn.removeAttr('disabled');
        } else {
          $btn.attr('disabled', 'disabled');
        }
      };
  mention($D, document, $editor, null, checkBtn);
  $D.on('keyup', '.tweet-editor', function() {
    checkBtn();
  });
  $D.on('focus', '.tweet-editor', function() {
    var $this = $(this);
    $('.tweet-placeholder').remove();
    $this.stop(true, true);
    $this.animate({
      'min-height': 60
    }, 160, function() {
      $toolbar.stop(true, true);
      $toolbar.fadeIn(160);
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
      $btn.click();
      $(this).blur();
    }
  });
  $D.on('click', '.tweet-submit', function(e) {
    e.preventDefault();
    var $this = $(this),
        $editor = $('.tweet-editor'),
        $tweetList = $('.tweet-list .item-list'),
        content = $editor.html(),
        text = $.trim($editor.text()),
        url = '/tweet/create';
    if (text.length) {
      $this.attr('disabled', 'disabled');
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
            if ($tweetList.length) {
              $tweetList.prepend(html);
            } else {
              $('.tweet-list').html('<ul class="item-list">' + html + '</ul>');
            }
            editorEmpty();
            $('#show-' + data.id).css({
                                   opacity: 0
                                 })
                                 .animate({
                                   opacity: 1
                                 });
          } else {
            $this.removeAttr('disabled');
            noty(data);
          }
        }
      });
    }
  });
  $D.on('click', '.retweet a', function(e) {
    e.preventDefault();
    var $this = $(this),
        $name_area = $this.parents('.item').find('a.name'),
        name = $name_area.attr('data-name'),
        nickname = $name_area.html(),
        user_url = $name_area.attr('href'),
        $textarea = $('.tweet-editor');

    $textarea.append('&nbsp;<a class="mention" data-username="' + name + '" href="'+ user_url +'">@' + nickname + '</a>&nbsp;');
    $textarea.focus();
    placeCaretAtEnd($textarea[0]);
    checkBtn();
  });
});
