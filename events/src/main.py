from fastapi import FastAPI, Depends, Form
import mysql.connector
from validate_token import validate_token  # assuming this is implemented



app = FastAPI()

@app.get("/event/health")
def health_check():
    return {"status": "ok"}



@app.get("/event/get-events")
def get_events(token=Depends(validate_token)):
    try:
        conn = mysql.connector.connect(
            host="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM EVENTS")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        
        return {
            "status": 200,
            "body": rows
        }
    except:
        return {
            "status": 500,
            "body": {"data": "Error occurred"}
        }

            
@app.post("/event/create-events")
def create_events(name: str = Form(...), time: str = Form(...), token=Depends(validate_token)):
    try:
        conn = mysql.connector.connect(
            host="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO events (name, time) VALUES (%s, %s)", (name, time))
        conn.commit()
                
        cur.close()
        conn.close()
        return {"status": 201, "body": {"data": "Event created"}}
    except Exception as e:
        return {"status": 500, "body": {"error": str(e)}}
    

