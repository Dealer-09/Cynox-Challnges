from flask import Flask, request, make_response, render_template_string
import hmac, hashlib, base64, json

app    = Flask(__name__)
SECRET = "avengers"   # weak secret — crackable with flask-unsign

def sign(data):
    payload = base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip('=')
    sig     = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha1).hexdigest()
    return f"{payload}.{sig}"

def verify(cookie):
    try:
        payload, sig = cookie.rsplit('.', 1)
        expected = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha1).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        return json.loads(base64.urlsafe_b64decode(payload + '=='))
    except:
        return None

TMPL = """
<!DOCTYPE html><html>
<head><title>Stark Tower — Access Control</title>
<style>
  body{background:#0a0a10;color:#ccc;font-family:monospace;padding:40px;}
  h2{color:#e8b800;} .box{border:1px solid #333;padding:20px;max-width:500px;}
  .ok{color:#4f4;} .err{color:#f44;} .warn{color:#fa0;}
  a{color:#e8b800;}
</style></head>
<body>
<h2>⚙ STARK TOWER — ACCESS CONTROL SYSTEM</h2>
{% if data %}
  <div class="box">
    <p>Welcome, <b>{{ data.user }}</b></p>
    <p>Role: <b>{{ data.role }}</b></p>
    {% if data.role == 'omega_level' %}
      <p class="ok">✓ OMEGA CLEARANCE GRANTED</p>
      <p class="ok">Flag: cyn0x{c00k13_f0rg3d_4cc3ss_gr4nt3d}</p>
    {% else %}
      <p class="warn">✗ Insufficient clearance. Omega Level required for this resource.</p>
    {% endif %}
  </div>
{% else %}
  <div class="box">
    <p>You are not authenticated.</p>
    <a href="/login">Login as field operative →</a>
  </div>
{% endif %}
</body></html>
"""

@app.route('/')
def index():
    cookie = request.cookies.get('session')
    data   = verify(cookie) if cookie else None
    return render_template_string(TMPL, data=data)

@app.route('/login')
def login():
    resp = make_response("Logged in. <a href='/'>Go back</a>")
    resp.set_cookie('session', sign({"user": "agent", "role": "field_operative"}))
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)