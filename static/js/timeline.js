$(function() {
  var $editor = $('.tweet-editor'),
      editorEmpty = function() {
        var $placeholder = $('<div class="tweet-placeholder">输入内容吧...</div>');
        $('.tweet-editor').html($placeholder)
                          .css({
                            'min-height': 19
                          });
        $('.tweet-box .toolbar').addClass('dn');
      },
      checkBtn = function() {
        var $editor = $('.tweet-editor'),
            $btn = $('.tweet-submmit'),
            text = $editor.text();
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
    $('.tweet-placeholder').remove();
    $(this).css({
      'min-height': 60
    });
    $('.tweet-box .toolbar').removeClass('dn');
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
  $D.on('click', '.tweet-submmit', function(e) {
    e.preventDefault();
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
            $btn.removeAttr('disabled');
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
