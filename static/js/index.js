$(function() {
  $('.index-nav').fix();
  $D.on('click', '.index-nav li a, .pagination li a', function(e) {
    e.preventDefault();
    var $this = $(this),
        $parent = $this.parent('li'),
        $ul = $this.parents('ul.nav'),
        $navWrap = $('.nav-wrap'),
        $pjaxContent = $('#pjax-content'),
        url = $this.attr('href'),
        hbk = function() {
          $this.parents('ul').find('li.on').addClass('on');
          $this.parent('li').removeClass('on');
        },
        cbk = function(d) {
          var $page = $('.pagination'),
              $nodeTag = $('.node .node-tag'),
              pageContent = $(d).find('.pagination').html();
          if (!$page.length) {
            $('.organ').after('<div class="pagination"></div>');
            $page = $('.pagination');
          }
          if (pageContent && pageContent !== '') {
            $page.html(pageContent);
          } else {
            $page.remove();
          }
          if ($nodeTag.length) {
            $nodeTag.next('.description').tooltip();
          }
        };
    $pjaxContent.pjaxHandler({
      url: url,
      ele: $this,
      cbk: cbk,
      hbk: hbk
    });
    $ul.find('li').removeClass('on');
    $parent.addClass('on');
  });
});
