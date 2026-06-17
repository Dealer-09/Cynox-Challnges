# Reference: server-side JWT verification logic (vulnerable)
# Accepts BOTH RS256 and HS256, using the SAME public key for both
# This is the algorithm confusion vulnerability.

import jwt

def verify(token, PUBLIC_KEY):
    for algo in ['RS256', 'HS256']:
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[algo])
            if payload.get('role') == 'director':
                return "ACCESS GRANTED"
            return f"Denied. Role: {payload.get('role')}"
        except Exception:
            continue
    return "Verification failed"
