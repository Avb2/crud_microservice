import time 
import uuid
from fastapi import FastAPI, HTTPException, Form, Response
from jose import jwt
import time, uuid
from pydantic import BaseModel

app = FastAPI()


class TokenRequest(BaseModel):
    username: str

app.router

@app.get("/auth/health")
def health_check():
    return {"status": "ok"}

@app.post("/auth/sign-up")
def issue_token(response: Response, username:str = Form(...), ):
    with open("/app/keys/ticket-priv-key.pem", "r") as file:
        priv = file.read()

    epoch_time = int(time.time())

    access_payload = {
        "sub": str(uuid.uuid4()),
        "username": username,
        "role": "user",
        "exp": epoch_time + 15 * 60,
        "iat": epoch_time,
        "type": "access"
    }

    refresh_payload = {
        "sub": str(uuid.uuid4()),
        "username": username,
        "exp": epoch_time + 7 * 24 * 60 * 60,
        "iat": epoch_time,
        "type": "refresh"
    }

    access_token = jwt.encode(access_payload, priv, algorithm="RS256")
    refresh_token = jwt.encode(refresh_payload, priv, algorithm="RS256")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=900 
    )



    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "data": "User Created!"
    }



@app.post("/auth/refresh-token")
def refresh_token(response: Response, access_token: str = Form(...)):
    try:
        with open("/app/keys/public.pem", "r") as file:
            pubkey = file.read()

        decoded = jwt.decode(access_token, pubkey, algorithms=["RS256"])
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired refresh token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    epoch_time = int(time.time())
    new_access = {
        "sub": str(uuid.uuid4()),
        "username": decoded["username"],
        "role": "user",
        "exp": epoch_time + 15 * 60,
        "iat": epoch_time,
        "type": "access"
    }
    new_refresh = {
        "sub": str(uuid.uuid4()),
        "username": decoded["username"],
        "exp": epoch_time + 7 * 24 * 60 * 60,
        "iat": epoch_time,
        "type": "refresh"
    }

    with open("/app/keys/ticket-priv-key.pem", "r") as file:
        priv = file.read()

    encoded_access = jwt.encode(new_access, priv, algorithm="RS256")
    encoded_refresh = jwt.encode(new_refresh, priv, algorithm="RS256")


    response.set_cookie(
        key="access_token",
        value=encoded_access,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=900 
    )



    response.set_cookie(
        key="refresh_token",
        value=encoded_refresh,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  
    )


    return {
        "access_token": encoded_access,
        "refresh_token": encoded_refresh
    }
