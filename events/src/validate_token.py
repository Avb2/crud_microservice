from fastapi import Request, HTTPException
from jose import jwt

def validate_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        with open("/app/keys/public.pem", "r") as file:
            pubkey = file.read()

        payload = jwt.decode(token, pubkey, algorithms=["RS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Expired token")