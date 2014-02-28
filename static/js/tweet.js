$(function() {
  $D.on('click', '.tweet-img-content', function() {
    var $this = $(this),
        $covers = $this.find('.img-cover'),
        $dns = $this.find('.img-cover.dn'),
        $tt = $this.prev('.thumbs'),
        $ul,
        $thumbs,
        $area = $this.parents('.tweet-img-area');
    if ($tt.length) {
        $ul = $tt.find('ul');
        $thumbs = $ul.find('li');
        $ul.width(($thumbs.outerWidth() + 10) * $thumbs.length);
    }
    if ($area.hasClass('close')) {
      $area.removeClass('close').addClass('open');
      if ($thumbs && $thumbs.length) {
        $thumbs.removeClass('cur');
        $thumbs.eq(0).addClass('cur');
      }
      $covers.hide();
      $covers.eq(0).show();
    } else {
      $area.removeClass('open').addClass('close');
      $covers.show();
      $dns.hide();
    }
  });
  $D.on('click', '.thumbs li', function() {
    var $this = $(this),
        $area = $this.parents('.tweet-img-area'),
        $ul = $this.parent('ul'),
        $thumbs = $ul.find('li'),
        $covers = $area.find('.img-cover'),
        idx = $thumbs.index($this[0]);
    $covers.hide();
    $covers.eq(idx).show();
    $thumbs.removeClass('cur');
    $this.addClass('cur');
  });
  $D.on('mousemove', '.thumbs', function(e) {
    var $this = $(this),
        $ul = $this.find('ul'),
        pos = e.pageX - $this.offset().left,
        posP = pos / $this.width(),
        listP = $ul.width() * posP,
        offset = pos - listP;
    if ($ul.width() > $this.width()) {
      $ul.css({
        'left': offset
      });
    }
  });
});
