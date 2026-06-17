<?php
$output = ""; $err = "";
$blacklist = ['cat ', 'ls ', 'whoami ', 'flag', ' '];
if (isset($_POST['cmd']) && !empty($_POST['cmd'])) {
    $cmd = $_POST['cmd'];
    $blocked = false;
    foreach ($blacklist as $word) {
        if (stripos($cmd, $word) !== false) { $blocked = true; break; }
    }
    if ($blocked) { $err = "Command blocked by S.H.I.E.L.D. Security Filter v1.0"; }
    else { $output = shell_exec($cmd . " 2>&1"); }
}
?>
<!-- S.H.I.E.L.D. Internal Diagnostic Panel — filters spaces, 'flag', 'cat ', 'ls ' -->
