$(function() {
  $D.on('click', '#add-music', function(e) {
    e.preventDefault();
    $('#music-select').click();
  });

  $('#music-select').fileupload({
    url: '/upload/music',
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10),
          status_msg = $('.status-msg');
      status_msg.addClass('loader-bar').html('音乐上传进度：' + progress + '%');
      if (progress === 100) {
        status_msg.removeClass('loader-bar').html('音乐上传完毕');
        setTimeout(function() {status_msg.html('');}, 500);
      }
    },
    done: function(e, result) {
      var status_msg = $('.status-msg'),
          waterfall = $('#post-page-waterfall'),
          post_id = $('#post_id').val(),
          data = result.result;
      if (data.status === "success") {
        ue.focus(true);
        ue.execCommand('inserthtml', '<audio controls><source src="' + data.path + '" type="' + data.content_type + '"></audio>');
      } else {
        status_msg.removeClass('loader-bar').html('音乐上传失败');
        noty(data);
      }
    }
  });
});
