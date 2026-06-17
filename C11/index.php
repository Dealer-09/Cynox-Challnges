<?php
$msg = ""; $err = "";
$blocked = ['php', 'php3', 'php4', 'php5', 'phtml'];
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['profile'])) {
    $file = $_FILES['profile'];
    $ext  = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (in_array($ext, $blocked)) {
        $err = "File type not allowed.";
    } else {
        move_uploaded_file($file['tmp_name'], __DIR__.'/uploads/'.basename($file['name']));
        $msg = "Profile photo uploaded successfully: ".basename($file['name']);
    }
}
?>
<!-- Stark Industries Employee Portal — Profile Upload -->
<!-- Apache config registers .php7 as a PHP handler (not in blacklist above) -->
