$(function() {
  var nav_top = $('.index-nav').offset().top,
  fix_nav_bar = function() {
    var top = $(document).scrollTop(),
        $shape = $('#shape'),
        $nav = $('.index-nav'),
        $nav_fixed = $('.index-nav.fixed'),
        $menu = $('#head .menu'),
        $menu_fixed = $('#head .menu.fixed'),
        $head = $('#head'),
        nav_width = $nav.width(),
        nav_height = $nav.height(),
        menu_left = $menu.offset().left,
        menu_height = $menu.height(),
        head_left = $head.offset().left;

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

  $D.scroll(function() {
    fix_nav_bar();
  });
});
