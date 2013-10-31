$(function () {
  $('.node-action a.btn').live('click', function() {
    var url = $(this).attr('href');
    var $info_follow_area = $(this).parents('.node-data').find('.node-info-follow');
    var content = $info_follow_area.html();
    var count = parseInt(content.substr(content.indexOf('</i>') + 4, content.length));
    var content_top = content.substr(0, content.indexOf('</i>') + 4);
    var $that = $(this);

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        $that.removeClass('onloading');
        if (data.type === 1) {
          $that.removeClass('fo').addClass('unfo');
          $that.html('已关注');
          count += 1;
          content = content_top + ' ' + count + ' 关注';
        } else if (data.type === 0) {
          $that.removeClass('unfo').addClass('fo');
          $that.html('关注');
          count -= 1;
          content = content_top + ' ' + count + ' 关注';
        }
        $info_follow_area.html(content);
      }
    });
    $that.addClass('onloading');
    button_content = $that.html();
    $that.html(button_content + ' ..');
    return false;
  });

  $('.node-tag li a').live('click', function() {
    var url = $(this).attr('href');
    var $node_information = $('.node-information');
    var $node_data = $('.node-data');
    var $that = $(this);

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        if ($that.parent('li').hasClass('description')) {
          var source =
            '<div id="show" class="node-description">'
          +   '<%== node_description %>'
          + '</div>';

          var render = template.compile(source);
          var html = render(data);
          var $description = $('div.node-description');
          var $relationship = $('div.node-relationship');
          if ($description.length > 0) {
            $description.remove();
          }
          if ($relationship.length > 0) {
            $relationship.remove();
          }
          if ($('.loading').length) {
            $('.loading').remove();
          }
          $node_information.html(html);
          var $show = $('#show');
          $show.hide().fadeIn();
        } else if ($that.parent('li').hasClass('relationship')) {
          var source =
            '<div id="show" class="node-relationship">'
          +   '<% if (parent_nodes.length > 0) { %>'
          +   '<div class="parent-nodes title">父节点</div>'
          +   '<ul class="parent-nodes">'
          +     '<% for (i=0; i < parent_nodes.length; i++) { %>'
          +       '<li id="<%= parent_nodes[i].urlname %>">'
          +         '<a href="<%= parent_nodes[i].url %>">'
          +           '<div class="node-tag">'
            +           '<img class="icon" align="absmiddle" src="<%= parent_nodes[i].icon %>">'
              +         '<span class="name">'
              +           '<%= parent_nodes[i].name %>'
              +         '</span>'
            +         '</div>'
            +         '<div class="description" tooltip="<%== parent_nodes[i].summary %>">'
            +           '<%== parent_nodes[i].summary %>'
            +         '</div>'
          +         '</a>'
          +       '</li>'
          +     '<% } %>'
          +   '</ul>'
          +   '<% } %>'
          +   '<% if (child_nodes.length > 0) { %>'
          +   '<div class="child-nodes title">子节点</div>'
          +   '<ul class="child-nodes">'
          +     '<% for (i=0; i < child_nodes.length; i++) { %>'
          +       '<li id="<%= child_nodes[i].urlname %>">'
          +         '<a href="<%= child_nodes[i].url %>">'
          +           '<div class="node-tag">'
            +           '<img class="icon" align="absmiddle" src="<%= child_nodes[i].icon %>">'
              +         '<span class="name">'
              +           '<%= child_nodes[i].name %>'
              +         '</span>'
            +         '</div>'
            +         '<div class="description" data-tooltip="<%== child_nodes[i].summary %>">'
            +           '<%== child_nodes[i].summary %>'
            +         '</div>'
          +         '</a>'
          +       '</li>'
          +     '<% } %>'
          +   '</ul>'
          +   '<% } %>'
          +   '<% if (sibling_nodes.length > 0) { %>'
          +   '<div class="sibling-nodes title">兄弟节点</div>'
          +   '<ul class="sibling-nodes">'
          +     '<% for (i=0; i < sibling_nodes.length; i++) { %>'
          +       '<li id="<%= sibling_nodes[i].urlname %>">'
          +         '<a href="<%= sibling_nodes[i].url %>">'
          +           '<div class="node-tag">'
            +           '<img class="icon" align="absmiddle" src="<%= sibling_nodes[i].icon %>">'
              +         '<span class="name">'
              +           '<%= sibling_nodes[i].name %>'
              +         '</span>'
            +         '</div>'
            +         '<div class="description" data-tooltip="<%== sibling_nodes[i].summary %>">'
            +           '<%== sibling_nodes[i].summary %>'
            +         '</div>'
          +         '</a>'
          +       '</li>'
          +     '<% } %>'
          +   '</ul>'
          +   '<% } %>'
          + '</div>';

          var render = template.compile(source);
          var html = render(data);
          var $description = $('div.node-description');
          var $relationship = $('div.node-relationship');
          if ($description.length > 0) {
            $description.remove();
          }
          if ($relationship.length > 0) {
            $relationship.remove();
          }
          if ($('.loading').length) {
            $('.loading').remove();
          }
          $node_information.html(html);
          var $show = $('#show');
          $show.hide().fadeIn();
        }
      }
    });
    if (!$that.hasClass('on')) {
      $that.parent('li').prev('li').removeClass('on');
      $that.parent('li').next('li').removeClass('on');
      $that.parent('li').addClass('on');
      var height = $node_information.height();
      if ($('.loading').length) {
        $('.loading').remove();
      }
      $node_information.html('<div class="loading"></div>');
      var margin_height = (height - 24) / 2;
      $('.loading').css({'margin-top': margin_height, 'margin-bottom': margin_height});
    }
    return false;
  });
  $('.node .node-tag').next('.description').tooltip();
  /*
  $('.node .description').on('mousemove', function(e) {
    if (!$('.tooltip').length) {
      var tooltip = '<div class="tooltip">' + $(this).html() + '</div>';
      $(tooltip).hide().appendTo('body').fadeIn();
    }
    $('.tooltip').css({'position': 'absolute',
                       'top': mousePosition(e).y + 15,
                       'left': mousePosition(e).x + 15
    });
  }).on('mouseout', function() {
    $('.tooltip').fadeOut(300);
    setTimeout(function() {$('.tooltip').remove();}, 300);
  });
  */
});
