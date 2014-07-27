$(function() {
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
    progressall: function(e, data){
      var progress = parseInt(data.loaded / data.total * 100, 10),
          status_msg = $('.status-msg');
      status_msg.addClass('loader-bar').html('图片上传进度：' + progress + '%');
      if( progress == 100 ){
        status_msg.removeClass('loader-bar').html('图片上传完毕');
        setTimeout(function() {status_msg.html('');}, 500);
      }
    },
    done: function(e, result){
      var status_msg = $('.status-msg'),
          waterfall = $('#post-page-waterfall'),
          post_id = $('#post_id').val(),
          data = result.result;

      if (data.status === "success") {
        data = data.data;
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-reply-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });

  $D.on('click', '.reply-create button', function(e) {
    e.preventDefault();
    var $this = $(this),
        url = window.location.href,
        xsrf = get_cookie('_xsrf'),
        content = ue.getContent(),
        args = {"content": content, "_xsrf": xsrf};

    $.post(url, $.param(args), function(data) {
      if (data.status !== 'success') {
        noty(data);
      } else {
        window.location.href = data.reply_url;
        return;
      }
    });
  });

  ue.addListener('ready', function() {
    ueReady();
  });

});
