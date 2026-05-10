from flask import Flask, request, jsonify, render_template_string
import jwt, json
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

with open('/app/private.pem','rb') as f: PRIVATE_KEY = f.read()
with open('/app/public.pem', 'rb') as f: PUBLIC_KEY  = f.read()

TMPL = """<!DOCTYPE html><html>
<head><title>S.W.O.R.D. Token Portal</title>
<style>body{background:#0a0a10;color:#ccc;font-family:monospace;padding:40px;}
h2{color:#7b2fff;} .box{border:1px solid #333;padding:20px;max-width:600px;}
.ok{color:#4f4;} .err{color:#f44;} pre{color:#0f0;background:#111;padding:10px;}</style>
</head><body>
<h2>⬡ S.W.O.R.D. DIRECTOR ACCESS PORTAL</h2>
<div class="box">
{% if flag %}<p class="ok">Director access granted.</p><p class="ok">{{ flag }}</p>
{% elif user %}<p class="err">Access denied. Director clearance required. Your role: {{ user.role }}</p>
{% else %}
<p>Submit your JWT token for verification.</p>
<form method="POST" action="/verify">
  <textarea name="token" rows="4" cols="60" style="background:#111;color:#0f0;border:1px solid #333;font-family:monospace;"></textarea><br><br>
  <button style="background:#7b2fff;color:#fff;border:none;padding:8px 16px;cursor:pointer;">Verify Token</button>
</form>
{% endif %}
</div>
<br><small><a href="/public.key" style="color:#444">Public Key</a></small>
</body></html>"""

@app.route('/')
def index(): return render_template_string(TMPL, flag=None, user=None)

@app.route('/login')
def login():
    token = jwt.encode({"user":"agent","role":"field_operative"}, PRIVATE_KEY, algorithm="RS256")
    return jsonify({"token": token, "note": "RS256 signed. Director access requires role=director."})

@app.route('/public.key')
def pubkey(): return PUBLIC_KEY, 200, {'Content-Type': 'text/plain'}

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form.get('token','').strip()
    try:
        # Vulnerable: accepts both RS256 and HS256 — the confusion attack
        for algo in ['RS256', 'HS256']:
            try:
                secret = PUBLIC_KEY if algo == 'HS256' else PUBLIC_KEY
                payload = jwt.decode(token, secret, algorithms=[algo])
                if payload.get('role') == 'director':
                    return render_template_string(TMPL, flag="cyn0x{jwt_4lg0_c0nfus10n_att4ck}", user=None)
                return render_template_string(TMPL, flag=None, user=payload)
            except: continue
        return render_template_string(TMPL, flag=None, user=None)
    except Exception as e:
        return render_template_string(TMPL, flag=None, user=None)

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)