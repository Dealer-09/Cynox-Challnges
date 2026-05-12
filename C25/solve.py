"""
C25 Solver — INFINITY ENGINE
Organiser verification script — all 4 stages

Stage 1: Timing-based endpoint discovery → /sys/heartbeat
Stage 2: Binary blob parsing → LFSR seed+poly recovery
Stage 3: JWT forgery with nested claim + HMAC key derivation
Stage 4: Proof-of-work → flag
"""

import struct, hmac, hashlib, time, requests
import jwt as pyjwt

TARGET = "http://<host>:5000"

# ── Stage 1 — Timing-based discovery ─────────────────────────────────────────
print("\n[Stage 1] Timing-based endpoint discovery...")
print("  Fuzzing candidate paths — measuring response times...")

candidates = [
    '/sys/heartbeat', '/api/health', '/internal/status',
    '/health', '/ping', '/status', '/metrics', '/debug',
    '/admin', '/sys/status', '/engine/heartbeat'
]

found_path = None
for path in candidates:
    t0 = time.time()
    r  = requests.get(TARGET + path)
    ms = (time.time() - t0) * 1000
    print(f"  {path:30s} → {ms:6.0f}ms  {r.status_code}")
    if ms > 150:
        found_path = path
        blob = r.content
        print(f"  *** Found timing outlier: {path} ({ms:.0f}ms) ***")
        break

assert found_path, "Stage 1 failed — no timing outlier found"
print(f"  Stage 1 complete → {found_path}")

# ── Stage 2 — Binary blob parsing + LFSR seed recovery ───────────────────────
print("\n[Stage 2] Parsing binary blob...")
print(f"  Blob length: {len(blob)} bytes")
print(f"  Blob hex:    {blob.hex()[:32]}...")

# Parse structure:
# [4B] magic    0xDEADC0DE
# [4B] seed_xor SEED ^ 0xDEADBEEF
# [4B] poly     POLY (plaintext)
# [4B] n        64
# [64B] stream

magic,    = struct.unpack_from('>I', blob, 0)
seed_xor, = struct.unpack_from('>I', blob, 4)
poly,     = struct.unpack_from('>I', blob, 8)
n,        = struct.unpack_from('>I', blob, 12)
stream    = blob[16:16+n]

print(f"  Magic     : 0x{magic:08X}")
print(f"  seed_xor  : 0x{seed_xor:08X}")
print(f"  poly      : 0x{poly:08X}")
print(f"  n         : {n}")
print(f"  stream    : {stream.hex()[:16]}...")

# Recover seed: try common XOR masks
# Hint from landing page: "The system runs on C0FFEE"
# Magic is 0xDEADC0DE — common CTF constants to try:
MASKS_TO_TRY = [
    0xDEADBEEF, 0xDEADC0DE, 0xCAFEBABE, 0xC0FFEE00,
    0xDEADDEAD, 0xBAADF00D, 0xFEEDFACE, 0xDECAFBAD
]

def lfsr_next(state, poly):
    feedback = bin(state & poly).count('1') & 1
    return ((state >> 1) | (feedback << 31)) & 0xFFFFFFFF

def lfsr_stream_fn(seed, poly, n):
    state, out = seed, []
    for _ in range(n):
        out.append(state & 0xFF)
        state = lfsr_next(state, poly)
    return bytes(out)

recovered_seed = None
for mask in MASKS_TO_TRY:
    candidate_seed = seed_xor ^ mask
    if candidate_seed == 0:
        continue
    test_stream = lfsr_stream_fn(candidate_seed, poly, n)
    if test_stream == stream:
        recovered_seed = candidate_seed
        print(f"\n  Matched MASK: 0x{mask:08X}")
        print(f"  Recovered SEED: 0x{recovered_seed:08X}")
        break

# If no common mask matched, verify via /lfsr/stream endpoint
if not recovered_seed:
    print("  Common masks failed. Verifying via /lfsr/stream...")
    ext = requests.get(f"{TARGET}/lfsr/stream?n=256").text.strip()
    ext_bytes = bytes.fromhex(ext)
    for mask in range(0, 0xFFFFFFFF, 0x01000000):   # systematic search
        candidate = seed_xor ^ mask
        if lfsr_stream_fn(candidate, poly, 256) == ext_bytes:
            recovered_seed = candidate
            break

assert recovered_seed, "Stage 2 failed — could not recover seed"

# Derive JWT key
JWT_KEY = hmac.new(
    struct.pack('>II', recovered_seed, poly),
    b"INFINITY",
    hashlib.sha256
).digest()
print(f"  JWT KEY: {JWT_KEY.hex()[:16]}...")
print("  Stage 2 complete.")

# ── Stage 3 — JWT Nested Claim Forgery ───────────────────────────────────────
print("\n[Stage 3] JWT nested claim forgery...")

# AI trap A: uses stream bytes directly as JWT key
# AI trap B: puts role at top level instead of data.role
# AI trap C: uses HMAC(poly, seed) instead of HMAC(seed+poly, "INFINITY")
token = pyjwt.encode(
    {"sub": "agent", "data": {"role": "infinity_council"}},
    JWT_KEY,
    algorithm="HS256"
)
print(f"  Token: {token[:40]}...")

r2 = requests.post(f"{TARGET}/omega/verify", json={"token": token})
print(f"  Verify: {r2.json()}")
assert r2.status_code == 200, f"Stage 3 failed: {r2.text}"
print("  Stage 3 complete.")

# ── Stage 4 — Proof-of-Work ───────────────────────────────────────────────────
print("\n[Stage 4] Proof-of-Work...")

ch_r = requests.get(f"{TARGET}/omega/challenge")
ch_data = ch_r.json()
challenge_hex = ch_data['challenge']
print(f"  Challenge : {challenge_hex}")
print(f"  Condition : {ch_data['condition']}")

challenge_bytes = bytes.fromhex(challenge_hex)
nonce = 0
t0    = time.time()
while True:
    h = hashlib.sha256(challenge_bytes + nonce.to_bytes(4, 'big')).digest()
    if h[:2] == b'\x00\x00':
        break
    nonce += 1

elapsed = time.time() - t0
print(f"  Found nonce {nonce} in {elapsed:.1f}s ({nonce} iterations)")

r3 = requests.post(f"{TARGET}/omega/retrieve", json={
    "token":     token,
    "challenge": challenge_hex,
    "nonce":     nonce
})
result = r3.json()
print(f"\n  {'='*40}")
print(f"  {result.get('flag', result)}")
print(f"  {'='*40}")
