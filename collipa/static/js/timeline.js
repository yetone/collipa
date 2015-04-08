$(function() {
  var $box = $('.tweet-box'),
      $editor = $('.tweet-editor'),
      $toolbar = $('.tweet-box .toolbar'),
      $btn = $('.tweet-submit'),
      editorEmpty = function(_$editor) {
        $editor = _$editor || $editor;
        $toolbar = $editor.parents('.tweet-box').find('.toolbar');
        var $placeholder = $('<div class="tweet-placeholder">输入内容吧...</div>');
        $editor.stop(true, true);
        $editor.html($placeholder)
        $box.removeClass('focus');
        $toolbar.animate({
          height: 0,
          padding: 0
        }, {
          duration: 500,
          complete: function() {
            $(this).css({
              display: 'none'
            });
          }
        });
      },
      checkBtn = function(_$editor, _$btn) {
        $editor = _$editor || $editor;
        $btn = _$btn || $btn;
        var text = $editor.text();
        if (text.trim().length >= 3) {
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
            url = window.location.pathname + '?from_id=' + id,
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
      };
  $.Collipa.mention($D, document, $editor, null, checkBtn);
  $D.on('input', '.tweet-editor', function() {
    var $this = $(this),
        $btn = $this.parents('.tweet-box').find('.tweet-submit');
    checkBtn($this, $btn);
  });
  $D.on('focus', '.tweet-editor', function() {
    var $this = $(this),
        $box = $this.parents('.tweet-box'),
        $toolbar = $box.find('.toolbar');
    if ($box.hasClass('focus')) return;
    $this.find('.tweet-placeholder').remove();
    $this.stop(true, true);
    $box.addClass('focus');
    $toolbar.css({
      display: 'block',
      height: 0,
      padding: 0
    }).animate({
      height: 34,
      paddingTop: 10,
      paddingBottom: 10
    }, {
      duration: 500
    });
  });
  $D.on('click', '.tweet-box', function(e) {
    e.stopPropagation();
  });
  $D.on('click', function() {
    var $this = $(this),
        text = $.trim($editor.text());
    if (text.length > 0) {
      return;
    }
    editorEmpty($editor);
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
        $layout = $('#layout');

    $layout.remove();
    $('body').append($('#tweet-editor-template').html());
    $('#layout').popslide({
      cbk: function() {
        var $textarea = $('#layout .tweet-editor');
        $textarea.append('@' + nickname + '&nbsp;');
        placeCaretAtEnd($textarea[0]);
        checkBtn($textarea, $('#layout .tweet-submit'));
        $.Collipa.mention($D, document, $textarea, null, function() {
          checkBtn($textarea, $('#layout .tweet-submit'));
        });
      }
    });
  });
  $('#pic-select').on('click', function(e) {
    e.stopPropagation();
  }).imageUpload({
    cbk: function(data) {
      var img = '<span class="img-cover"><img data-id="' + data.id + '" src="' + data.path + '"><i class="icon-remove-circle"></i></span>',
          $area = $('.tweet-preview');
      $area.append(img);
      checkPreview();
    }
  });
  $D.on('click', '.add-img', function(e) {
    e.preventDefault();
    $('#pic-select').click();
  });
  $D.on('click', '.tweet-preview .img-cover i', function() {
    var $this = $(this),
        $imgCover = $this.parent('.img-cover'),
        id = $imgCover.find('img').data('id'),
        url = '/image/' + id;
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
  $editor.focus();
});
