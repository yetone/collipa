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

function waterfall() {
  var $imgs = $('.image-item'),
      hl = [0, 0, 0],
      marginTop = 20,
      marginLeft = 20;
  $imgs.each(function(i, e) {
    var $img = $(e),
        width = $img.width(),
        height = width / $img.data('width') * $img.data('height'),
        min = hl.min(),
        minIndex = hl.minIndex();
    $img.css({
      left: minIndex * (marginLeft + width),
      top: min + marginTop
    });
    hl[minIndex] = min + height + marginTop;
    console.log(hl);
  });
  $('.image-list').height(hl.max() + 20);
}

$(function() {
  waterfall();
});
