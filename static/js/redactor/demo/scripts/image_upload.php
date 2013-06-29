<?php

// This is a simplified example, which doesn't cover security of uploaded images.
// This example just demonstrate the logic behind the process.


// files storage folder
$dir = '/home/web/sitecom/images/';

$_FILES['file']['type'] = strtolower($_FILES['file']['type']);

if ($_FILES['file']['type'] == 'image/png'
|| $_FILES['file']['type'] == 'image/jpg'
|| $_FILES['file']['type'] == 'image/gif'
|| $_FILES['file']['type'] == 'image/jpeg'
|| $_FILES['file']['type'] == 'image/pjpeg')
{
    // setting file's mysterious name
    $filename = md5(date('YmdHis')).'.jpg';
    $file = $dir.$filename;

    // copying
    move_uploaded_file($_FILES['file']['tmp_name'], $file);

    // displaying file
	$array = array(
		'filelink' => 'http://redactor8/tmp/'.$filename
	);

	echo stripslashes(json_encode($array));

}

?>