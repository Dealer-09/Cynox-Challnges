<?php
// Asgard CMS — Admin login: admin / thor (hardcoded)
// Theme installer blocks: php, php3, php4, php5, php7, phtml — NOT phar
define('ADMIN_USER', 'admin');
define('ADMIN_PASS', 'thor');
$blocked = ['php','php3','php4','php5','php7','phtml'];
// ... upload handler checks extension against $blocked, .phar passes through
