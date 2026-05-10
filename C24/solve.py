"""
C24 Solver — Ultron's Core

Steps:
1. Run pyinstxtractor on the binary to extract .pyc files
   $ python3 pyinstxtractor.py ultron_core  (binary not provided here — .pyc is the extracted artifact)

2. Decompile the .pyc:
   $ python3 -m decompile3 ultron_core.pyc  OR  uncompyle6 ultron_core.pyc

3. Recovered source shows:
   - _x = [116,104,52,110,111,115,95,115,110,52,112]  → b"th4nos_sn4p"
   - Key derived via: base64.urlsafe_b64encode(hashlib.sha256(seed).digest())
   - Encrypted blob stored as 'blob'

AI trap: AI extracts the raw key bytes from _x and tries them directly as Fernet key.
         Fernet requires base64url-encoded 32-byte key (SHA256 output → b64encode).
         Skipping the SHA256+b64 step gives: "Invalid token" / key format error.
"""
import base64, hashlib
from cryptography.fernet import Fernet

_x   = [116,104,52,110,111,115,95,115,110,52,112]
seed = bytes(_x)
key  = base64.urlsafe_b64encode(hashlib.sha256(seed).digest())
f    = Fernet(key)

blob = b'gAAAAABp_0S4SnTiVckOvzol_5KWJ5axp4pZwFu_rgEb3d2X7-cVGhPMtSQKbiZQxsdZEL9oTWAAAU5cdXRT9fhn6ZZIAdqNE4Xvq_5GEzZzMV_6YbuHiHccOWkNS2yMOyfg_y_8sYyp'
print(f.decrypt(blob).decode())
# Output: cyn0x{py1nst4ll3r_f3rn3t_l4y3r_cr4ck3d}