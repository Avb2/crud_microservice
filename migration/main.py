import mysql.connector


def create_tables():
    try:
        conn = mysql.connector.connect(
            host="eventsdb.cluster-c1qc6uswoceq.us-east-2.rds.amazonaws.com",
            user="alex",
            passwd="password",
            database="mydb"
        )
        cur = conn.cursor()

        create_users_table = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """

        create_events_table = """
        CREATE TABLE events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            time INTEGER NOT NULL
        )
        """

        create_tickets_table = """
        CREATE TABLE tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            userid VARCHAR(255) NOT NULL
        )
        """
        
        cur.execute(create_users_table)
        cur.execute(create_events_table)
        cur.execute(create_tickets_table)
        conn.commit()
                
        cur.close()
        conn.close()
            
    except Exception as e:
        print(e)


if __name__ == "__main__":
    create_tables()