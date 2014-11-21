/**
 * Created by yetone on 14-7-13.
 */
Array.prototype.min = function() {
  return Math.min.apply(Math, this);
};

Array.prototype.max = function() {
  return Math.max.apply(Math, this);
};

Array.prototype.minIndex = function() {
  var min = this.min();
  return this.indexOf(min);
};

Array.prototype.maxIndex = function() {
  var min = this.max();
  return this.indexOf(max);
};

function waterfall(opt, undefined) {
  opt = $.extend({
    selector: '.image-item',
    wrapper: '.image-list',
    src: '.image-src'
  }, opt);
  var $imgs = $(opt.selector),
      $wrapper = $(opt.wrapper),
      hl = [];
  if (!opt.width) {
    opt.width = $imgs.width();
  }
  if (opt.marginLeft === undefined) {
    opt.marginLeft = $imgs.css('margin-left');
  }
  if (opt.marginTop === undefined) {
    opt.marginTop = $imgs.css('margin-top');
  }
  if (!opt.count) {
    opt.count = Math.floor($wrapper.width() / (opt.width + opt.marginLeft));
  }
  for (var i = 0; i < opt.count; i++) {
    hl.push(0);
  }

  $imgs.each(function(i, e) {
    var $img = $(e),
        $src = $img.find(opt.src),
        height = opt.width / $src.data('width') * $src.data('height'),
        min = hl.min(),
        minIndex = hl.minIndex();
    $img.css({
      left: minIndex * (opt.marginLeft + opt.width),
      top: min + opt.marginTop,
      display: 'block'
    });
    $img.width(opt.width);
    $img.find('img').width(opt.width);
    hl[minIndex] = min + height + opt.marginTop;
    $wrapper.height(hl.max() + 20);
  });
}

function initWaterfall() {
  var marginTop = marginLeft = 20,
      count = 3,
      width = 220,
      wWidth = $(window).width();
  if (wWidth < 720) {
    marginTop = marginLeft = 10;
    count = 2;
  }
  width = (wWidth - (count + 1) * marginLeft) / count;
  waterfall({
    marginTop: marginTop,
    marginLeft: marginLeft,
    width: width,
    count: count
  });
}
$(function() {
  initWaterfall();
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
          type: 'DELETE',
          success: function(jsn) {
            noty(jsn);
            obj.cbk();
            if (jsn.status === 'success') {
              console.log(jsn);
              $image.animate({opacity: 0}, 800, function() {
                $(this).remove();
                initWaterfall();
              });
            }
          }
        });
      }
    });
  });

  G.imageLoadedId = [];
  function loadNextPage() {
    var $images = $('.image-item'),
        fromId = $images.last().data('id'),
        albumId = $('.image-list-wrap').data('album-id'),
        url = '/image/list/?album_id=' + albumId + '&from_id=' + fromId,
        pageLoading = new G.PageLoading();

    if (pageLoading.isLoading() || typeof fromId !== 'number' || G.imageLoadedId.indexOf(fromId) >= 0) {
      return;
    }
    G.imageLoadedId.push(fromId);
    pageLoading.start();


    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'JSON',
      success: function(data) {
        pageLoading.stop();
        var source = $('#image-list-template').html(),
            render = template.compile(source),
            html = render(data);
        $('.image-list').append(html);
        initWaterfall();
      }
    })
  }

  $W.on('scroll', function() {
    ($(document).scrollTop() + $(window).height() > $(document).height() - G.autoLoadHeight) && loadNextPage();
  });
});
