from fastapi import FastAPI, Depends, Form
import mysql.connector
from validate_token import validate_token  # assuming this is implemented



app = FastAPI()

@app.get("/get-events")
def get_events(token=Depends(validate_token)):
    try:
        with mysql.connector.connect(
            host="db",
            user="alex",
            passwd="password",
            database="mydb"
        ) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM EVENTS")
            rows = cur.fetchall()
            return {
                "status": 200,
                "body": rows
            }
    except:
        return {
            "status": 500,
            "body": {"data": "Error occurred"}
        }

            
@app.post("/create-events")
def create_events(name: str = Form(...), time: str = Form(...), token=Depends(validate_token)):
    try:
        with mysql.connector.connect(
            host="db",
            user="alex",
            passwd="password",
            database="mydb"
        ) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO events (name, time) VALUES (%s, %s)", (name, time))
            conn.commit()
            return {"status": 201, "body": {"data": "Event created"}}
    except Exception as e:
        return {"status": 500, "body": {"error": str(e)}}
