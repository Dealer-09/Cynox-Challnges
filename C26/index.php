<?php
$msg = "";
$err = "";

// Blacklist check — blocks known PHP extensions
$blocked = ['php', 'php3', 'php4', 'php5', 'phtml'];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['profile'])) {
    $file    = $_FILES['profile'];
    $name    = $file['name'];
    $tmp     = $file['tmp_name'];
    $ext     = strtolower(pathinfo($name, PATHINFO_EXTENSION));

    if (in_array($ext, $blocked)) {
        $err = "File type not allowed. Only images are accepted.";
    } elseif ($file['size'] > 500000) {
        $err = "File too large.";
    } else {
        $dest = __DIR__ . '/uploads/' . basename($name);
        move_uploaded_file($tmp, $dest);
        $msg = "Profile photo uploaded successfully: <a href='uploads/" . htmlspecialchars(basename($name)) . "'>" . htmlspecialchars(basename($name)) . "</a>";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<title>Stark Industries — Employee Portal</title>
<style>
  body { background: #0d0d0d; color: #ccc; font-family: monospace; padding: 40px; }
  h1   { color: #e8b800; }
  h3   { color: #aaa; }
  input[type=file] { color: #ccc; }
  button { background: #e8b800; color: #000; border: none; padding: 8px 20px; cursor: pointer; font-weight: bold; }
  .msg  { color: #4caf50; margin-top: 15px; }
  .err  { color: #f44336; margin-top: 15px; }
  .box  { border: 1px solid #333; padding: 20px; max-width: 500px; margin-top: 20px; }
</style>
</head>
<body>
<h1>⚙ STARK INDUSTRIES</h1>
<h3>Employee Self-Service Portal — Profile Photo Upload</h3>
<p>Upload your employee profile photo. Only image files are permitted.</p>
<div class="box">
  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="profile"><br><br>
    <button type="submit">Upload Photo</button>
  </form>
  <?php if ($msg) echo "<p class='msg'>$msg</p>"; ?>
  <?php if ($err) echo "<p class='err'>$err</p>"; ?>
</div>
<br>
<small style="color:#444">Stark Industries IT Security — v3.1.4 | Powered by PHP</small>
</body>
</html>