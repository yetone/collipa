/**
 * Created by yetone on 14-7-13.
 */

$(function() {
  function initWaterfall($items, done) {
    var spacingWidth,
        spacingHeight = spacingWidth = 10,
        count = 3,
        wWidth = $('.image-list').outerWidth();
    if (wWidth < 600) {
      spacingHeight = spacingWidth = 10;
      count = 2;
    }
    var width = (wWidth - (count + 1) * spacingWidth) / count;
    ($items || $('.image-item')).waterfall({
      wrapperSelector: '.image-list',
      imageSelector: '.image-src',
      spacingHeight: spacingHeight,
      spacingWidth: spacingWidth,
      marginTop: 10,
      width: width,
      count: count,
      isFadeIn: true,
      done: done
    });
  }

  $('.image-list').hammer({
    hold_timeout: 1000,
    stop_browser_behavior: {userSelect: ''}
  }).on('hold', '.image-item', function(e) {
    if (!$('.image-list-wrap').data('access')) return;
    e.preventDefault();
    var $this = $(this);
    $this.addClass('waiting')
      .addClass('animate')
      .append('<div class="confirm"><i title="删除" class="delete icon-remove-sign"></i></div>');
  });

  $D.on('click', function() {
    var $waitings = $('.image-item.waiting');
    $waitings.each(function(_, e) {
      $(e).find('.confirm').remove();
    });
    $waitings.removeClass('waiting').removeClass('animate');
  });

  $D.on('click', '.image-item,#request', function(e) {
    e.preventDefault();
    e.stopPropagation();
  });

  $D.on('click', '.image-item .delete', function(e) {
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this),
        $image = $this.parents('.image-item');
    $.Collipa.request({
      content: '确定删除？',
      ok: function(obj) {
        $.ajax({
          url: $image.find('.image-p').data('href'),
          type: 'DELETE'
        }).done(function(jsn) {
          noty(jsn);
          obj.cbk();
          if (jsn.status !== 'success') {
            return;
          }
          $image.animate({opacity: 0}, 800, function() {
            $(this).remove();
          });
        });
      }
    });
  });

  function loadNextPage() {
    var $wrapper = $('.image-list'),
        $images = $wrapper.find('.image-item'),
        fromId = $images.last().data('id'),
        albumId = $('.image-list-wrap').data('album-id'),
        url = '/image/list/',
        data = {
          album_id: albumId,
          from_id: fromId
        },
        pageLoading = new G.PageLoading();

    if ($wrapper.prop('over') || pageLoading.isLoading()) {
      return;
    }

    pageLoading.start();

    $.ajax({
      type: 'GET',
      url: url,
      data: data
    }).done(function(jsn) {
      $wrapper.prop('over', !jsn.data.has_more);
      if ($wrapper.prop('over')) {
        pageLoading.stop();
      }
      var source = $('#image-list-template').html(),
          render = template.compile(source),
          html = render(jsn.data),
          $items = $(html);
      $('.image-list').append($items);
      $items = $items.filter(function() {
        return this.nodeType === 1;
      });
      initWaterfall($items, function() {
        pageLoading.stop();
      });
    });
  }

  initWaterfall(null, function() {
    $W.on('scroll', function() {
      ($(document).scrollTop() + $(window).height() > $(document).height() - G.autoLoadHeight) && loadNextPage();
    });
  });
});
