$(function(){
  var xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
  function updateCoords(c)
  {
    $('#x').val(c.x);
    $('#y').val(c.y);
    $('#w').val(c.w);
    $('#h').val(c.h);
  };

  function checkCoords()
  {
    if (parseInt($('#w').val())) return true;
    alert('请在大图截取一部分作为头像');
    return false;
  };

  function showPreview(coords) {
    var rx = 100 / coords.w;
    var ry = 100 / coords.h;

    $('#preview').css({
        width: Math.round(rx * data.width ) + 'px',
        height: Math.round(ry * data.height ) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
        });
  };

  function hidePreview() {
    $('#preview').stop().fadeOut('fast');
  };

  $('#btn-avatar-cancel').click(function(){
    $('.jcrop-holder').remove();
    $('#target').remove();
    $('#img-select').html("<img id='target'>");
    $('.hide-coat').show();
    $('#avatar-cropper').hide();
    $('.avatar-show img').show();
    $('#avatar-status').hide();
  });
  $('#btn-avatar-done').click(function(){
    var $that = $(this);

    var x = parseInt($('#x').val());
    var y = parseInt($('#y').val());
    var w = parseInt($('#w').val());
    var h = parseInt($('#h').val());
    var src = $('#src').val();
    var args = {
      "x": x,
      "y": y,
      "w": w,
      "h": h,
      "src": src
    };
    args._xsrf = xsrf;
    $.post('/account/setting/avatar/crop', $.param(args), function(data){
      if(data.status == 'success'){
        $that.html('确认');
        $('.jcrop-holder').remove();
        $('#target').remove();
        $('#img-select').html("<img id='target'>");
        $('.hide-coat').show();
        $('#avatar-cropper').hide();
        $('.avatar-show img').show();
        $('#avatar-status').hide();

        $('.avatar-show img').attr('src', data.avatar);
        $('#avatar-src').val(data.src);
      }
    });
    $that.html('正在保存..');
  });
  $('#pic-select').fileupload({
    url: '/upload/avatar?_xsrf=' + xsrf,
    type: 'POST',
    dataType: 'json',
    sequentialUploads: true,
    autoUpload: true,
    progressall: function(e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      $('.avatar-show img').hide();
      $('#avatar-status').show();
      $('#avatar-status p').html('正在上传头像...' + progress + '%');
    },
    done: function(e, result) {
      data = result.result;
      if(data.status == "success"){
        $('.hide-coat').hide();
        $('#avatar-cropper').show();
        var width = parseInt(data.width);
        var height = parseInt(data.height);
        var c_width = 200;
        var c_height = c_width;
        var shape_width = $('#avatar-cropper').width();
        if( width > shape_width ){
          height = parseInt(height / width * shape_width);
          width = shape_width;
          c_width = parseInt(c_width * width / shape_width);
          c_height = c_width;
        }
        $('#avatar-cropper #img-select img').attr('src', data.src);
        $('#src').val(data.src);
        $('#target').Jcrop({
          aspectRatio: 1,
          onSelect: updateCoords,
          setSelect: [0,0,c_width,c_height],
          boxWidth: width,
          boxHeight: height
        });
      } else {
        noty({text: data.message, type: data.status});
        $('.avatar-show img').show();
        $('#avatar-status').hide();
      }
    },
  });
  $('#set-avatar-btn').click(function() {
    $('#pic-select').click();
    return false;
    });

});

