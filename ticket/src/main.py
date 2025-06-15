from fastapi import FastAPI, Depends, Form, HTTPException
import mysql.connector
from validate_token import validate_token

app = FastAPI()

@app.post("/new-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...), token=Depends(validate_token)):
    try:
        with mysql.connector.connect(
            host ="db",
            user="alex",
            passwd="password",
            database="mydb"

            ) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO tickets (name, userid) VALUES (%s, %s)", (name, userid))
                conn.commit()

    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": "New ticket created"}
    }
    




@app.delete("/cancel-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...), token=Depends(validate_token)):
    try:
         with mysql.connector.connect(
            host ="db",
            user="alex",
            passwd="password",
            database="mydb"

            ) as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM tickets WHERE name = %s AND userid = %s", (name, userid))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Ticket not found")
                conn.commit()

    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": "Ticket cancelled"}
    }


@app.get("/verify-ticket")
def create_ticket(name: str = Form(...), userid: str = Form(...), token=Depends(validate_token)):
    try:
        with mysql.connector.connect(
            host ="db",
            user="alex",
            passwd="password",
            database="mydb"

            ) as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM tickets WHERE name = %s AND userid = %s", (name, userid))
                tickets = cur.fetchall()


    except mysql.connector.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
          raise HTTPException(status_code=400, detail="An error occurred")
    
    return {
          "status": 200,
          "body": {"data": tickets}
    }