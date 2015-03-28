<?php

// This is a simplified example, which doesn't cover security of uploaded files.
// This example just demonstrate the logic behind the process.

move_uploaded_file($_FILES['file']['tmp_name'], '/files/'.$_FILES['file']['name']);

$array = array(
	'filelink' => '/files/'.$_FILES['file']['name'],
	'filename' => $_FILES['file']['name']
);

echo stripslashes(json_encode($array));

?>