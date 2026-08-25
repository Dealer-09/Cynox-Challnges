<?php
$output = "";
$err    = "";

// Filter: blocks spaces and common commands directly
// Bypass: use $IFS as space substitute, or use 'tac' instead of 'cat'
$blacklist = ['cat ', 'ls ', 'whoami ', 'flag', ' '];

if (isset($_POST['cmd']) && !empty($_POST['cmd'])) {
    $cmd = $_POST['cmd'];
    $blocked = false;
    foreach ($blacklist as $word) {
        if (stripos($cmd, $word) !== false) {
            $blocked = true;
            break;
        }
    }
    if ($blocked) {
        $err = "Command blocked by S.H.I.E.L.D. Security Filter v1.0";
    } else {
        $output = shell_exec($cmd . " 2>&1");
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<title>S.H.I.E.L.D. Internal — Diagnostic Panel</title>
<style>
  body { background: #080810; color: #ccc; font-family: monospace; padding: 40px; }
  h2 { color: #e8b800; }
  input[type=text] { background: #111; color: #0f0; border: 1px solid #333; padding: 8px; width: 400px; font-family: monospace; }
  button { background: #e8b800; color: #000; border: none; padding: 8px 16px; cursor: pointer; font-weight: bold; }
  pre { background: #0a0a0a; border: 1px solid #222; padding: 15px; color: #0f0; white-space: pre-wrap; }
  .err { color: #f44; margin-top: 10px; }
</style>
</head>
<body>
<h2>⚠ S.H.I.E.L.D. INTERNAL — SERVER DIAGNOSTIC PANEL</h2>
<p style="color:#555">Restricted access. Authorised personnel only.</p>
<form method="POST">
  <input type="text" name="cmd" placeholder="Enter diagnostic command..." autocomplete="off">
  <button type="submit">Run</button>
</form>
<?php if ($err)    echo "<p class='err'>$err</p>"; ?>
<?php if ($output) echo "<pre>" . htmlspecialchars($output) . "</pre>"; ?>
<br><small style="color:#222">Security filter active. Suspicious commands will be logged.</small>
</body>
</html>