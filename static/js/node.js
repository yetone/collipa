$(function () {
  $D.on('click', '.node-action a.btn', function(e) {
    e.preventDefault();
    var $this = $(this),
        url = $this.attr('href'),
        $info_follow_area = $this.parents('.node-data').find('.node-info-follow'),
        content = $info_follow_area.html(),
        count = parseInt(content.substr(content.indexOf('</i>') + 4, content.length)),
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
    var $this = $(this),
        url = $this.attr('href'),
        $node_information = $('.node-information'),
        $node_data = $('.node-data');

    $.get(url, function(data) {
      var source,
          render,
          html,
          $description,
          $relationship,
          $show = $('#show');
      if (data.status !== 'success') {
        noty(data);
      } else {
        if ($this.parent('li').hasClass('description')) {
          source =
                '<div id="show" class="node-description">'+
                   '<%== node_description %>'+
                 '</div>';
          render = template.compile(source);
          html = render(data);
          $description = $('div.node-description');
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
          $show.hide().fadeIn();
        } else if ($this.parent('li').hasClass('relationship')) {
          source = $('#node-template').html();
          render = template.compile(source);
          html = render(data);
          $description = $('div.node-description');
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
  $('.nav-wrap li a, .pagination li a').pjax({
    container: '#pjax-content',
    part: '#pjax-content',
    success: function() {
      var $no = $('.nav-wrap li.on'),
          $nbs;
      if ($no.length) {
        $nbs = $no.parents('.nav-wrap').find('.nav-bottom-span');
        setTimeout(function() {
          $no.trigger('mouseover');
          if ($nbs.length) {
            $nbs.css({'opacity': 1});
          }
        }, 300);
      }
    }
  });
});
