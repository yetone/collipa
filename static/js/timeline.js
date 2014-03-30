$(function() {
  var $editor = $('.tweet-editor'),
      $toolbar = $('.tweet-box .toolbar'),
      $btn = $('.tweet-submit'),
      editorEmpty = function(_$editor) {
        $editor = _$editor || $editor;
        $toolbar = $editor.parents('.tweet-box').find('.toolbar');
        var $placeholder = $('<div class="tweet-placeholder">输入内容吧...</div>');
        $editor.stop(true, true);
        $editor.html($placeholder)
                          .animate({
                            'min-height': 19
                          }, 160);
        if ($toolbar.length) {
          $toolbar.stop(true, true);
          $toolbar.fadeOut(160);
        }
      },
      checkBtn = function(_$editor, _$btn) {
        $editor = _$editor || $editor;
        $btn = _$btn || $btn;
        var text = $editor.text();
        if (text.length >= 3) {
          $btn.removeAttr('disabled');
        } else {
          $btn.attr('disabled', 'disabled');
        }
      },
      previewEmpty = function() {
        var $preview = $('.tweet-preview');
        $preview.html('');
        checkPreview();
      },
      checkPreview = function() {
        var $preview = $('.tweet-preview');
        if ($preview.find('img').length > 0) {
          $preview.removeClass('dn');
        } else {
          $preview.addClass('dn');
        }
      },
      loadedId = [],
      loadNextPage = function() {
        var $ul = $('.tweet-list .item-list'),
            $lis = $ul.find('li.item'),
            id = $lis.last().data('id'),
            url = '/timeline?from_id=' + id,
            $ploading = $('<span class="ploading style-2"></span>');
        if (loadedId.indexOf(id) !== -1) {
          return;
        }
        loadedId.push(id);
        if (!$('.ploading').length) {
          $('body').append($ploading);
        }
        $.ajax({
          url: url,
          type: 'GET',
          dataType: 'html',
          success: function(d) {
            var $c = $(d).find('.tweet-list li.item');
            $ul.append($c);
            $ploading = $('.ploading');
            $ploading.animate(
              {opacity: 0},
              function() {
                $ploading.remove();
              }
            );
          }
        });
      },
      blurTimer;
  $.Collipa.mention($D, document, $editor, null, checkBtn);
  $D.on('keyup', '.tweet-editor', function() {
    var $this = $(this),
        $btn = $this.parents('.tweet-box').find('.tweet-submit');
    checkBtn($this, $btn);
  });
  $D.on('focus', '.tweet-editor', function() {
    var $this = $(this),
        $parent = $this.parents('.tweet-box'),
        $toolbar = $parent.find('.toolbar');
    $this.find('.tweet-placeholder').remove();
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
      blurTimer = setTimeout(function() {
        editorEmpty($this);
      }, 400);
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
        $parent = $this.parents('.tweet-box'),
        $editor = $parent.find('.tweet-editor'),
        $imgs = $parent.find('.tweet-preview img'),
        $tweetList = $('.tweet-list .item-list'),
        content = $editor.html(),
        text = $.trim($editor.text()),
        image_ids = [],
        url = '/tweet/create';
    if (text.length) {
      $this.attr('disabled', 'disabled');
      $imgs.each(function(i, e) {
        var $e = $(e);
        image_ids.push($e.data('id'));
      });
      $.ajax({
        url: url,
        type: 'post',
        data: {
          content: content,
          image_ids: image_ids.join(','),
          '_xsrf': get_cookie('_xsrf')
        },
        success: function(data) {
          if (data.status === 'success') {
            var source = $('#tweet-template').html(),
                render = template.compile(source),
                html = render(data),
                $layout = $('.tweet-editor-layout');
            if ($tweetList.length) {
              $tweetList.prepend(html);
            } else {
              $('.tweet-list').html('<ul class="item-list">' + html + '</ul>');
            }
            //editorEmpty();
            previewEmpty();
            $editor.html('').focus();
            $('#show-' + data.id).css({
                                   opacity: 0
                                 })
                                 .animate({
                                   opacity: 1
                                 });
            if ($layout.length) {
              $layout.find('.layout-close').click();
              noty(data);
            }
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
        $layout = $('#layout');

    $layout.remove();
    $('body').append($('#tweet-editor-template').html());
    $('#layout').popslide({
      cbk: function() {
        var $textarea = $('#layout .tweet-editor');
        $textarea.append('&nbsp;<a class="mention" data-username="' + name + '" href="'+ user_url +'">@' + nickname + '</a>&nbsp;');
        placeCaretAtEnd($textarea[0]);
        checkBtn($textarea, $('#layout .tweet-submit'));
      }
    });
  });
  $('#pic-select').imageUpload({
    cbk: function(data) {
      var img = '<span class="img-cover"><img data-id="' + data.id + '" src="' + data.path + '"><i class="icon-remove-circle"></i></span>',
          $area = $('.tweet-preview');
      $area.append(img);
      checkPreview();
    }
  });
  $D.on('click', '.add-img', function(e) {
    e.preventDefault();
    clearTimeout(blurTimer);
    $editor.focus();
    $('#pic-select').click();
  });
  $D.on('click', '.tweet-preview .img-cover i', function() {
    var $this = $(this),
        $imgCover = $this.parent('.img-cover'),
        id = $imgCover.find('img').data('id'),
        url = '/image/' + id;
    clearTimeout(blurTimer);
    $editor.focus();
    $.ajax({
      url: url + '?_xsrf=' + get_cookie('_xsrf'),
      type: 'DELETE',
      success: function(jsn) {
        $imgCover.fadeOut(function() {
          $(this).remove();
        });
        noty(jsn);
      }
    });
  });
  $W.on('scroll', function() {
    ($(document).scrollTop() + $(window).height() > $(document).height() - 300) && loadNextPage();
  });
});
