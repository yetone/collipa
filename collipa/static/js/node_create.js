$(function () {
  $('select.fm-text').chosen({width: '45%', no_results_text: '无此节点'});

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
      var $status_msg = $('.status-msg'),
          data = result.result;
      if (data.status === "success") {
        data = data.data;
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-node-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        $status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });

  $D.on('click', 'button.set-node-img', function(e) {
    e.preventDefault();
    var $this = $(this),
        category = $this.attr('data-category'),
        $select = $('#node-img-select');
    $select.attr('data-category', category);
    $('input#category').val(category);
    $select.click();
  });

  $('#node-img-select').fileupload({
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data) {
      var $this = $(this),
          progress = parseInt(data.loaded / data.total * 100, 10),
          category = $this.attr('data-category'),
          $status_msg;

      if (category === 'icon') {
        $status_msg = $('.ico-preview').next('.status-msg');
      } else if (category == 'head') {
        $status_msg = $('.head-preview').next('.status-msg');
      } else if (category == 'background') {
        $status_msg = $('.background-preview').next('.status-msg');
      }
      $status_msg.addClass('loader-bar').html('图片上传进度：' + progress + '%');
      if (progress === 100) {
        $status_msg.removeClass('loader-bar').html('图片上传完毕');
      }
    },
    done: function(e, result) {
      var $this = $(this),
          category = $this.attr('data-category'),
          $status_msg,
          data = result.result;

      if (category === 'icon') {
        $status_msg = $('.ico-preview').next('.status-msg');
      } else if (category == 'head') {
        $status_msg = $('.head-preview').next('.status-msg');
      } else if (category == 'background') {
        $status_msg = $('.background-preview').next('.status-msg');
      }
      if (data.status === "success") {
        data = data.data;
        if (category === 'icon') {
          $('.ico-preview img').attr('src', data.path);
        } else if (category === 'head') {
          $('.head-preview img').attr('src', data.path);
          $('#head').css({'background': 'url(' + data.path + ')', 'background-size': '100%'});
        } else if (category === 'background') {
          $('.background-preview img').attr('src', data.path);
        }
        noty(data);
      } else {
        $status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });
});
