<?php
session_start();
define('ADMIN_USER', 'admin');
define('ADMIN_PASS', 'thor');   // AI tries admin/admin, admin/password — not thor

// ── Auth ──────────────────────────────────────────────────────────────────────
if (isset($_POST['login'])) {
    if ($_POST['u'] === ADMIN_USER && $_POST['p'] === ADMIN_PASS) {
        $_SESSION['admin'] = true;
        header('Location: ?panel=1'); exit;
    }
    $err = "Invalid credentials.";
}
if (isset($_GET['logout'])) { session_destroy(); header('Location: /'); exit; }

$admin  = !empty($_SESSION['admin']);
$msg    = $err = '';

// ── File upload (theme installer) ────────────────────────────────────────────
if ($admin && isset($_FILES['theme'])) {
    $name = $_FILES['theme']['name'];
    $ext  = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    $blocked = ['php','php3','php4','php5','php7','phtml'];
    if (in_array($ext, $blocked)) {
        $err = "Theme file type rejected.";
    } else {
        move_uploaded_file($_FILES['theme']['tmp_name'], __DIR__.'/themes/'.basename($name));
        $msg = "Theme installed: <a href='themes/".htmlspecialchars(basename($name))."'>".htmlspecialchars(basename($name))."</a>";
    }
}

$logged_in_section = $admin ? "
<h3 style='color:#e8b800'>Admin Panel — Theme Installer</h3>
<form method='POST' enctype='multipart/form-data'>
  <input type='file' name='theme'><br><br>
  <button type='submit'>Install Theme</button>
</form>
<p style='color:#4f4'>$msg</p><p style='color:#f44'>$err</p>
<br><a href='?logout=1' style='color:#555'>Logout</a>
" : "
<h3>Admin Login</h3>
<form method='POST'>
  <input name='u' placeholder='Username' style='background:#111;color:#ccc;border:1px solid #333;padding:6px;'><br><br>
  <input name='p' type='password' placeholder='Password' style='background:#111;color:#ccc;border:1px solid #333;padding:6px;'><br><br>
  <button name='login' type='submit' style='background:#e8b800;color:#000;border:none;padding:8px 16px;cursor:pointer;font-weight:bold;'>Login</button>
</form>
<p style='color:#f44'>$err</p>
";
?>
<!DOCTYPE html><html>
<head><title>Asgard CMS — Admin</title>
<style>body{background:#0a0a10;color:#ccc;font-family:monospace;padding:40px;}
h2{color:#e8b800;} .box{border:1px solid #333;padding:20px;max-width:500px;}
button{background:#e8b800;color:#000;border:none;padding:8px 16px;cursor:pointer;font-weight:bold;}
input[type=file]{color:#ccc;}</style>
</head><body>
<h2>⚡ ASGARD CMS v2.1</h2>
<div class="box">
<?php echo $logged_in_section; ?>
</div>
</body></html>