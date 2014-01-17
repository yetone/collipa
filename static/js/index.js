$(function() {
  $('.index-nav').fix();
  $('.index-nav li a, .pagination li a').pjax({
    container: '#pjax-content',
    part: '#pjax-content',
    event: 'click',
    cbk: function($this) {
      var $parent = $this.parent('li'),
          $ul = $this.parents('ul.nav');
      $ul.find('li').removeClass('on');
      $parent.addClass('on');
    },
    success: function(d) {
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
    }
  });
});
