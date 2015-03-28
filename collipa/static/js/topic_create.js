$(function () {
  $('select.fm-text').chosen({width: '145px', no_results_text: '无此节点'});
  $D.on('click', '.topic-create button', function(e) {
    e.preventDefault();
    var $this = $(this),
        node_name = $('select').val(),
        title = $('input#fm-title').val(),
        url = window.location.href,
        $textarea = $('#ueditor_0').contents().find('body'),
        xsrf = get_cookie('_xsrf'),
        content = ue.getContent(),
        args = {"node_name": node_name, "title": title, "content": content, "_xsrf": xsrf};

    $(this).attr('disabled', 'disabled').addClass('onloading').html("正在创建...");
    $.post(url, $.param(args), function(data) {
      $this.removeAttr('disabled').removeClass("onloading").html("创建");
      if (data.status !== 'success') {
        noty(data);
      } else {
        window.location.href = data.topic_url;
        return;
      }
    });
  });

  $D.on('click', '.edui-for-myinsertimage', function(e) {
    e.preventDefault();
    $('#pic-select').click();
  });

  $('#pic-select').fileupload({
    url: '/image/upload?_xsrf=' + get_cookie('_xsrf'),
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10),
          $status_msg = $('.status-msg');
      $status_msg.addClass('loader-bar').html('图片上传进度：' + progress + '%');
      if (progress === 100) {
        $status_msg.removeClass('loader-bar').html('图片上传完毕');
      }
    },
    done: function(e, result) {
      var $status_msg = $('.status-msg');
      data = result.result;
      if (data.status === "success") {
        data = data.data;
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-topic-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        $status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });

  ue.addListener('ready', function() {
    ueReady();
  });

});
