<?php
// Wakanda Digital Archive — Document Viewer
// Blocklist covers passwd/shadow/hosts but NOT log files
$file = $_GET['file'] ?? 'welcome.html';
$blocked = ['passwd', 'shadow', 'hosts'];
foreach ($blocked as $b) {
    if (stripos($file, $b) !== false) { die("Access denied."); }
}
include($file);
// Server runs nginx — log path is /var/log/nginx/access.log, NOT apache2
