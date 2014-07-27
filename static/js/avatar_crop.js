$(function(){
  var xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
  function updateCoords(c) {
    $('#x').val(c.x);
    $('#y').val(c.y);
    $('#w').val(c.w);
    $('#h').val(c.h);
  }

  function checkCoords() {
    if (parseInt($('#w').val())) return true;
    alert('请在大图截取一部分作为头像');
    return false;
  }

  function showPreview(coords) {
    var rx = 100 / coords.w;
    var ry = 100 / coords.h;

    $('#preview').css({
        width: Math.round(rx * data.width ) + 'px',
        height: Math.round(ry * data.height ) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
        });
  }

  function hidePreview() {
    $('#preview').stop().fadeOut('fast');
  }

  $D.on('click', '#btn-avatar-cancel', function() {
    $('.jcrop-holder').remove();
    $('#target').remove();
    $('#img-select').html("<img id='target'>");
    $('.hide-coat').show();
    $('#avatar-cropper').hide();
    $('.avatar-show img').show();
    $('#avatar-status').hide();
  });

  $D.on('click', '#btn-avatar-done', function() {
    var $this = $(this),
        x = parseInt($('#x').val()),
        y = parseInt($('#y').val()),
        w = parseInt($('#w').val()),
        h = parseInt($('#h').val()),
        src = $('#src').val(),
        args = {
          "x": x,
          "y": y,
          "w": w,
          "h": h,
          "src": src
        };
    args._xsrf = xsrf;
    $.post('/account/setting/avatar/crop', $.param(args), function(data) {
      if (data.status == 'success') {
        $this.html('确认');
        $('.jcrop-holder').remove();
        $('#target').remove();
        $('#img-select').html("<img id='target'>");
        $('.hide-coat').show();
        $('#avatar-cropper').hide();
        $('.avatar-show img').show();
        $('#avatar-status').hide();

        $('.avatar-show img').attr('src', data.data.avatar);
        $('#avatar-src').val(data.data.src);
      }
    });
    $this.html('正在保存..');
  });
  $('#avatar-select').fileupload({
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
        data = data.data;
        $('.hide-coat').hide();
        $('#avatar-cropper').show();
        var width = parseInt(data.width),
            height = parseInt(data.height),
            c_width = 200,
            c_height = c_width,
            shape_width = $('#avatar-cropper').width();
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
  $D.on('click', '#set-avatar-btn', function(e) {
    e.preventDefault();
    $('#avatar-select').click();
  });
});

