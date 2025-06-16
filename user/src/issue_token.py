import requests
from fastapi import Response, HTTPException


def issue_token(username: str, response: Response):
    try:
        # Sends POST request to auth service to get tokens
        auth_res = requests.post(
            "http://auth-service.internal:5001/auth/issue-token",
            json={"username": username},
            headers={"Content-Type": "application/json"},
            timeout=5 
        )

        if auth_res.status_code != 200:
            print(auth_res.status_code)
            print(auth_res.text)
            raise HTTPException(status_code=502, detail="Token service failed")
        
        # Get the tokens from the response
        tokens = auth_res.json()

        if "access_token" not in tokens:
            raise HTTPException(status_code=500, detail="Token missing in response")

        # Set the access token
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=900 
        )


        if "refresh_token" in tokens:
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh_token"],
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=7 * 24 * 60 * 60  
            )

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=504, detail="Auth service unreachable")
