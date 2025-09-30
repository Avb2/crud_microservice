from fastapi import FastAPI, Response, HTTPException, Form, Request
import bcrypt
import mysql.connector
from issue_token import issue_token 
from jose import jwt
import requests


app = FastAPI()


@app.get("/user/health")
def health_check():
    return {"status": "ok"}

@app.post("/user/sign-up")
def sign_up(username: str = Form(...), password: str = Form(...), response: Response = None):
    try:
        conn = mysql.connector.connect(
            host="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"
        )
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Username already exists")

        hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pwd))
        

        issue_token(username, response)

        conn.commit()

                
        cur.close()
        conn.close()
        return {"status": 200, "body": {"data": "Login successful"}}

    except HTTPException as e:
        raise e
    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")

@app.post("/user/sign-in")
def sign_in(username: str = Form(...),
    password: str = Form(...),
    response: Response = None):
    try:
    #     conn = mysql.connector.connect(
    #         host="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
    #         user="alex",
    #         passwd="password",
    #         database="mydb"

    #     )
    #     cur = conn.cursor()
    #     cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    #     result = cur.fetchone()

                
    #     cur.close()
    #     conn.close()

    #     if not result or not bcrypt.checkpw(password.encode(), result[0].encode()):
    #         raise HTTPException(status_code=401, detail="Invalid username or password")

        issue_token(username, response)
        return {"status": 200, "body": {"data": "Login successful"}}

    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")

@app.post("/user/refresh-session")
def refresh_session(
    request: Request,
    response: Response,
    username: str = Form(...)
    ):

    try:
        conn = mysql.connector.connect(
            host="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"

        ) 
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

                
        cur.close()
        conn.close()

    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error")
    
    if result:
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Missing refresh token")
        
        try:
            auth_res = requests.post(
                "http://auth:5000/auth/refresh-token",
                data={"access_token": refresh_token}, 
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=5
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

        tokens = auth_res.json()

        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=True,
            samesite="Strict"
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="Strict"
        )


        

