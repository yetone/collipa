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
        height = opt.width / $img.data('width') * $img.data('height'),
        min = hl.min(),
        minIndex = hl.minIndex();
    $img.css({
      left: minIndex * (opt.marginLeft + opt.width),
      top: min + opt.marginTop,
      display: 'block'
    });
    hl[minIndex] = min + height + opt.marginTop;
    $wrapper.height(hl.max() + 20);
  });
}

$(function() {
  waterfall({
    marginTop: 20,
    marginLeft: 20,
    count: 3
  });
});
