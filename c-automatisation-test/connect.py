import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="traducteur",
        password="traducteur",
        port="3307",
        database="traducteur",
        ssl_disabled=False  # Activer SSL
    )
    if conn.is_connected():
        print("Connected to MySQL database")
except Error as e:
    print(f"Error connecting to MySQL: {e}")


