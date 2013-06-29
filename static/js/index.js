var nav_top = $('.index-nav').offset().top;
$(function() {
  var fix_nav_bar = function() {
    var top = $(document).scrollTop();
    var $shape = $('#shape');
    var $nav = $('.index-nav');
    var $nav_fixed = $('.index-nav.fixed');
    var $menu = $('#head .menu');
    var $menu_fixed = $('#head .menu.fixed');
    var $head = $('#head');
    var nav_width = $nav.width();
    var nav_height = $nav.height();
    var menu_left = $menu.offset().left;
    var menu_height = $menu.height();
    var head_left = $head.offset().left;

    if (top >= nav_top) {
      if (!$nav_fixed.length) {
        var menu_top = (parseInt(nav_height) - parseInt(menu_height)) / 2;
        $nav_fixed = $nav.clone();
        $menu_fixed = $menu.clone();
        $nav_fixed.addClass('fixed').css({'width': nav_width});
        $nav.after($nav_fixed);
        $menu_fixed.addClass('fixed').css({'right': +head_left + 20 + 'px', 'top': menu_top + 'px'});
        $menu_fixed.insertAfter($menu).hide().fadeIn(600);
      }
    } else {
      $nav_fixed.remove();
      $menu_fixed.remove();
    }
  };

  fix_nav_bar();

  $(document).scroll(function() {
    fix_nav_bar();
  });
});
