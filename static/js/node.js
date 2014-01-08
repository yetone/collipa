$(function () {
  $D.on('click', '.node-action a.btn', function(e) {
    e.preventDefault();
    var $this = $(this);
    var url = $this.attr('href'),
        $info_follow_area = $this.parents('.node-data').find('.node-info-follow');
    var content = $info_follow_area.html();
    var count = parseInt(content.substr(content.indexOf('</i>') + 4, content.length)),
        content_top = content.substr(0, content.indexOf('</i>') + 4);

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        $this.removeClass('onloading');
        if (data.type === 1) {
          $this.removeClass('fo').addClass('unfo');
          $this.html('已关注');
          count += 1;
          content = content_top + ' ' + count + ' 关注';
        } else if (data.type === 0) {
          $this.removeClass('unfo').addClass('fo');
          $this.html('关注');
          count -= 1;
          content = content_top + ' ' + count + ' 关注';
        }
        $info_follow_area.html(content);
      }
    });
    $this.addClass('onloading');
    button_content = $this.html();
    $this.html(button_content + ' ..');
  });

  $D.on('click', '.node-tag li a', function(e) {
    e.preventDefault();
    var $this = $(this);
    var url = $this.attr('href'),
        $node_information = $('.node-information'),
        $node_data = $('.node-data');

    $.get(url, function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        if ($this.parent('li').hasClass('description')) {
          var source =
            '<div id="show" class="node-description">'
          +   '<%== node_description %>'
          + '</div>';

          var render = template.compile(source);
          var html = render(data),
              $description = $('div.node-description'),
              $relationship = $('div.node-relationship');

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
        } else if ($this.parent('li').hasClass('relationship')) {
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
            +         '<div class="description" data-tooltip="<%== parent_nodes[i].summary %>">'
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
          var html = render(data),
              $description = $('div.node-description'),
              $relationship = $('div.node-relationship');

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
          $('.node .node-tag').next('.description').tooltip();
        }
      }
    });
    if (!$this.hasClass('on')) {
      $this.parent('li').prev('li').removeClass('on');
      $this.parent('li').next('li').removeClass('on');
      $this.parent('li').addClass('on');
      var height = $node_information.height();
      if ($('.loading').length) {
        $('.loading').remove();
      }
      $node_information.html('<div class="loading"></div>');
      var margin_height = (height - 24) / 2;
      $('.loading').css({'margin-top': margin_height, 'margin-bottom': margin_height});
    }
  });
  $('.node .node-tag').next('.description').tooltip();
});
