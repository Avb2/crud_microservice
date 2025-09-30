from fastapi import FastAPI, Depends, Form, HTTPException
import mysql.connector
from validate_token import validate_token

app = FastAPI()

@app.get("/ticket/health")
def health_check():
    return {"status": "ok"}


@app.post("/ticket/new-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...)):
    try:
        conn = mysql.connector.connect(
            host ="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"

            )
        cur = conn.cursor()
        cur.execute("INSERT INTO tickets (name, userid) VALUES (%s, %s)", (name, userid))
        conn.commit()

                
        cur.close()
        conn.close()

    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": "New ticket created"}
    }
    




@app.delete("/ticket/cancel-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...), token=Depends(validate_token)):
    try:
        conn = mysql.connector.connect(
            host ="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"

            )
        cur = conn.cursor()
        cur.execute("DELETE FROM tickets WHERE name = %s AND userid = %s", (name, userid))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")
        conn.commit()

                
        cur.close()
        conn.close()

    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": "Ticket cancelled"}
    }


@app.get("/ticket/verify-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...), token=Depends(validate_token)):
    try:
        conn = mysql.connector.connect(
            host ="eventsdb-instance-1.c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"

            )
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM tickets WHERE name = %s AND userid = %s", (name, userid))
        tickets = cur.fetchall()

                
        cur.close()
        conn.close()


    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": tickets}
    }