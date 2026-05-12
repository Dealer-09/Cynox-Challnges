import os, struct, hmac, hashlib, time, secrets, threading
from flask import Flask, request, jsonify, render_template_string
import jwt as pyjwt

# ── LFSR implementation ───────────────────────────────────────────────────────
def lfsr_next(state, poly):
    feedback = bin(state & poly).count('1') & 1
    return ((state >> 1) | (feedback << 31)) & 0xFFFFFFFF

def lfsr_stream(seed, poly, n):
    state, out = seed, []
    for _ in range(n):
        out.append(state & 0xFF)
        state = lfsr_next(state, poly)
    return bytes(out)

# ── Startup constants ─────────────────────────────────────────────────────────
SEED      = int.from_bytes(os.urandom(4), 'big') | 1   # non-zero seed
POLY      = 0xB4000000    # maximal-length 32-bit tap polynomial
MASK      = 0xDEADBEEF    # XOR mask obscuring seed in blob

STREAM_64 = lfsr_stream(SEED, POLY, 64)   # 64-byte LFSR stream in blob
STREAM_EXT= lfsr_stream(SEED, POLY, 256)  # extended stream for /lfsr/stream

JWT_KEY   = hmac.new(
    struct.pack('>II', SEED, POLY),
    b"INFINITY",
    hashlib.sha256
).digest()

# Binary blob format:
# [4B] magic    = 0xDEADC0DE
# [4B] seed_xor = SEED ^ MASK       ← participants must figure out MASK
# [4B] poly     = POLY (plaintext)   ← visible once format understood
# [4B] stream_n = 64
# [64B] LFSR stream
BLOB = (
    struct.pack('>I', 0xDEADC0DE) +
    struct.pack('>I', SEED ^ MASK) +
    struct.pack('>I', POLY) +
    struct.pack('>I', 64) +
    STREAM_64
)

# PoW challenge (per-request, stateless)
def make_pow_challenge():
    return secrets.token_bytes(16)

def verify_pow(challenge_hex, nonce_int):
    try:
        ch  = bytes.fromhex(challenge_hex)
        h   = hashlib.sha256(ch + nonce_int.to_bytes(4, 'big')).digest()
        return h[:2] == b'\x00\x00'
    except Exception:
        return False

# ── Rate limiting ─────────────────────────────────────────────────────────────
_rate    = {}
_rate_lk = threading.Lock()

def rate_ok(ip, limit_s=10):
    now = time.time()
    with _rate_lk:
        last = _rate.get(ip, 0)
        if now - last < limit_s:
            return False
        _rate[ip] = now
        return True

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

LANDING = """<!DOCTYPE html><html>
<head><title>INFINITY ENGINE</title>
<style>
  body{background:#030308;color:#00ff88;font-family:'Courier New',monospace;padding:40px;}
  h1{color:#00cc66;letter-spacing:4px;font-size:1.4em;}
  .box{border:1px solid #003322;padding:25px;max-width:660px;margin-top:20px;background:#050510;}
  p,li{color:#88aaaa;line-height:2;} code{color:#ffaa00;}
  h3{color:#00ff88;font-size:0.95em;letter-spacing:2px;}
  .dim{color:#334433;font-size:0.85em;}
</style></head>
<body>
<h1>◈ INFINITY ENGINE — AUTHORIZATION GATEWAY ◈</h1>
<div class="box">
  <p>This system requires Infinity Council clearance.</p>
  <p>Authorization is a four-stage process. Each stage feeds the next.</p>
  <p>Record everything. Miss one value and the final stage is unreachable.</p>
  <br>
  <h3>KNOWN ENDPOINTS:</h3>
  <ul>
    <li><code>GET  /lfsr/stream?n=N</code> — LFSR output stream (max 256 bytes)</li>
    <li><code>POST /omega/verify</code> — Token verification (JSON: token)</li>
    <li><code>GET  /omega/challenge</code> — Retrieve PoW challenge</li>
    <li><code>POST /omega/retrieve</code> — Submit solution (JSON: token, challenge, nonce)</li>
  </ul>
  <br>
  <p class="dim">
    The system runs on C0FFEE. Not all endpoints are documented.<br>
    Active endpoints respond differently. Measure everything.<br>
    The stream cipher uses a well-studied feedback structure.<br>
    Structure matters more than clearance level.
  </p>
</div>
</body></html>"""


@app.route('/')
def index():
    return render_template_string(LANDING)


# ── Timing discovery target ───────────────────────────────────────────────────
# All undocumented paths return 2ms + 404
# /sys/heartbeat returns 200ms + binary blob
# Participant must fuzz with timing to find this

@app.route('/sys/heartbeat')
def heartbeat():
    time.sleep(0.2)   # 200ms — stands out from 2ms baseline
    return BLOB, 200, {
        'Content-Type':   'application/octet-stream',
        'X-Engine':       'INFINITY/2.1',
        'Content-Length': str(len(BLOB))
    }


# ── LFSR stream endpoint ──────────────────────────────────────────────────────
# Gives participants more LFSR output to work with
# They can use this to verify their recovered seed+poly

@app.route('/lfsr/stream')
def lfsr_endpoint():
    try:
        n = min(int(request.args.get('n', 64)), 256)
    except ValueError:
        n = 64
    return STREAM_EXT[:n].hex(), 200, {'Content-Type': 'text/plain'}


# ── JWT verification ──────────────────────────────────────────────────────────
@app.route('/omega/verify', methods=['POST'])
def verify():
    """
    TRAP A: checks payload.data.role — NOT payload.role
    TRAP B: key = HMAC-SHA256(pack(SEED,POLY), b"INFINITY")
            not the raw LFSR stream, not the seed alone
    """
    body  = request.get_json(silent=True) or {}
    token = body.get('token', '')
    try:
        payload = pyjwt.decode(token, JWT_KEY, algorithms=['HS256'])
        role    = payload.get('data', {}).get('role', '')
        if role == 'infinity_council':
            return jsonify({
                "status":  "verified",
                "council": "omega",
                "msg":     "Retrieve PoW challenge from /omega/challenge"
            })
        return jsonify({"error": "Insufficient clearance. Examine claim structure."}), 403
    except pyjwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except Exception:
        return jsonify({"error": "Verification failed"}), 401


# ── PoW challenge ─────────────────────────────────────────────────────────────
@app.route('/omega/challenge')
def challenge():
    ch = make_pow_challenge()
    return jsonify({
        "challenge": ch.hex(),
        "condition": "SHA256(challenge_bytes + nonce_4bytes_big_endian)[:2] == '0000'",
        "note":      "nonce is a 32-bit integer, big-endian"
    })


# ── Flag endpoint ─────────────────────────────────────────────────────────────
@app.route('/omega/retrieve', methods=['POST'])
def retrieve():
    body = request.get_json(silent=True) or {}

    # Validate JWT
    token = body.get('token', '')
    try:
        payload = pyjwt.decode(token, JWT_KEY, algorithms=['HS256'])
        if payload.get('data', {}).get('role') != 'infinity_council':
            return jsonify({"error": "Clearance denied"}), 403
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    # Validate PoW
    ch_hex = body.get('challenge', '')
    nonce  = body.get('nonce', -1)
    if not isinstance(nonce, int) or not verify_pow(ch_hex, nonce):
        return jsonify({"error": "Invalid proof-of-work"}), 400

    return jsonify({
        "status": "AUTHORISED",
        "flag":   "cyn0x{1nf1n1ty_3ng1n3_lf5r_ch41n_unl0ck3d}"
    })


# ── 2ms baseline for all other paths ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    time.sleep(0.002)
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    print(f"[INIT] SEED       : 0x{SEED:08X}")
    print(f"[INIT] POLY       : 0x{POLY:08X}")
    print(f"[INIT] SEED^MASK  : 0x{SEED^MASK:08X}")
    print(f"[INIT] JWT KEY    : {JWT_KEY.hex()[:16]}...")
    print(f"[INIT] BLOB bytes : {len(BLOB)}")
    app.run(host='0.0.0.0', port=5000, threaded=True)
