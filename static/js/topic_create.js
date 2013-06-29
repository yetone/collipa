$(function () {
  $('select.fm-text').chosen({width: '145px', no_results_text: '无此节点'});
  $('.topic-create button').live('click', function() {
    var $that = $(this);
    var node_name = $('select').val();
    var title = $('input#fm-title').val();
    var url = window.location.href;
    var $textarea = $('#ueditor_0').contents().find('body');

    var xsrf = get_cookie('_xsrf');
    var content = ue.getContent();

    var args = {"node_name": node_name, "title": title, "content": content, "_xsrf": xsrf};

    $.post(url, $.param(args), function(data) {
      $that.removeAttr('disabled');
      if (data.status !== 'success') {
        noty(data);
      } else {
        window.location.href = data.topic_url;
        return;
      }
    });
    $(this).attr('disabled', 'disabled');
    return false;
  });

  $('.edui-for-myinsertimage').live('click', function() {
    $('#pic-select').click();
    return false;
  });
  $('#pic-select').fileupload({
    url: '/image/upload?_xsrf=' + get_cookie('_xsrf'),
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data){
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var $status_msg = $('.status-msg');
      $status_msg.addClass('loader-bar').html('图片上传进度：' + progress + '%');
      if( progress == 100 ){
        $status_msg.removeClass('loader-bar').html('图片上传完毕');
      }
    },
    done: function(e, result){
      var $status_msg = $('.status-msg');
      data = result.result;
      if(data.status == "success"){
        ue.focus(true);
        ue.execCommand('inserthtml', '<img class="upload-topic-image" src="' + data.path + '" style="max-width:480px;">');
      } else {
        $status_msg.removeClass('loader-bar').html('图片上传失败');
        noty(data);
      }
    }
  });
  ue.addListener('ready', function() {
    $('#ueditor_0').contents().find('body').keypress(function(e) {
      if (e.ctrlKey && e.which == 13 || e.which == 10) {
        $('.topic-create button').click();
      }
    });
  });
});
